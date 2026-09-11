from django.http import HttpResponse
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q, Sum, Avg, F
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from .models import (
    User, State, AYUSHFormulation, GITag, Patent, BiopiracyCase,
    Alert, TKDL_Entry, DashboardStat, IPActivity, AYUSHCategory, BiopiracyCaseStatus
)
from .serializers import (
    UserSerializer, UserCreateSerializer, StateSerializer, AYUSHFormulationSerializer,
    GITagSerializer, PatentSerializer, BiopiracyCaseSerializer, AlertSerializer,
    TKDL_EntrySerializer, DashboardStatSerializer, IPActivitySerializer,
    KPIResponseSerializer, StateAnalyticsSerializer, ComparisonRequestSerializer
)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in ['ADMIN', 'MINISTRY', 'ANALYST']


class IsMinistryOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['ADMIN', 'MINISTRY']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminOrReadOnly()]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def switch_language(self, request):
        lang = request.data.get('language', 'en')
        if lang in ['en', 'hi']:
            request.user.preferred_language = lang
            request.user.save()
            return Response({'language': lang})
        return Response({'error': 'Invalid language'}, status=status.HTTP_400_BAD_REQUEST)


class StateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = State.objects.filter(is_active=True)
    serializer_class = StateSerializer
    permission_classes = [IsAuthenticated]


class AYUSHFormulationViewSet(viewsets.ModelViewSet):
    queryset = AYUSHFormulation.objects.select_related('state_of_origin').all()
    serializer_class = AYUSHFormulationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filterset_fields = ['category', 'is_registered', 'state_of_origin', 'digitized_in_tkdl']
    search_fields = ['name', 'sanskrit_name', 'ingredients']


class GITagViewSet(viewsets.ModelViewSet):
    queryset = GITag.objects.select_related('state').all()
    serializer_class = GITagSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filterset_fields = ['state', 'status', 'category', 'is_ayush_related']
    search_fields = ['name', 'product', 'applicant', 'registration_number']

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        state_id = request.query_params.get('state')
        qs = self.get_queryset()
        if state_id:
            qs = qs.filter(state_id=state_id)

        stats = {
            'total': qs.count(),
            'registered': qs.filter(status='REGISTERED').count(),
            'pending': qs.filter(status='PENDING').count(),
            'by_category': dict(qs.values('category').annotate(count=Count('id')).values_list('category', 'count')),
            'by_state': dict(qs.values('state__name').annotate(count=Count('id')).values_list('state__name', 'count')[:10]),
        }
        return Response(stats)


class PatentViewSet(viewsets.ModelViewSet):
    queryset = Patent.objects.all()
    serializer_class = PatentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filterset_fields = ['country', 'status', 'ayush_category', 'is_biopiracy_suspect', 'applicant']
    search_fields = ['title', 'applicant', 'application_number', 'inventors', 'ipc_codes']

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        qs = self.get_queryset()
        stats = {
            'total': qs.count(),
            'by_status': dict(qs.values('status').annotate(count=Count('id')).values_list('status', 'count')),
            'by_category': dict(qs.values('ayush_category').annotate(count=Count('id')).values_list('ayush_category', 'count')),
            'by_country': dict(qs.values('country').annotate(count=Count('id')).values_list('country', 'count')),
            'biopiracy_suspects': qs.filter(is_biopiracy_suspect=True).count(),
            'granted': qs.filter(status='GRANTED').count(),
        }
        return Response(stats)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        days = int(request.query_params.get('days', 30))
        since = timezone.now() - timedelta(days=days)
        recent = self.get_queryset().filter(filing_date__gte=since.date())
        serializer = self.get_serializer(recent[:50], many=True)
        return Response(serializer.data)


class BiopiracyCaseViewSet(viewsets.ModelViewSet):
    queryset = BiopiracyCase.objects.select_related('patent', 'formulation', 'assigned_to').all()
    serializer_class = BiopiracyCaseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filterset_fields = ['status', 'priority', 'assigned_to', 'country_of_origin']
    search_fields = ['description', 'patent__title', 'formulation__name']

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        case = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            case.assigned_to = user
            case.save()
            IPActivity.objects.create(
                activity_type='BIOPIRACY_DETECTED',
                title=f"Case assigned: {case.patent.title[:50]}",
                description=f"Assigned to {user.get_full_name()}",
                related_user=user,
                metadata={'case_id': str(case.id)}
            )
            return Response({'message': 'Assigned successfully'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        case = self.get_object()
        notes = request.data.get('resolution_notes', '')
        case.status = BiopiracyCaseStatus.RESOLVED
        case.resolution_notes = notes
        case.resolved_date = timezone.now()
        case.save()

        IPActivity.objects.create(
            activity_type='BIOPIRACY_RESOLVED',
            title=f"Biopiracy case resolved: {case.patent.title[:50]}",
            description=f"Case {case.id} resolved by {request.user.get_full_name()}",
            related_user=request.user,
            metadata={'case_id': str(case.id)}
        )
        return Response({'message': 'Case resolved'})

    @action(detail=False, methods=['get'])
    def dashboard_summary(self, request):
        qs = self.get_queryset()
        summary = {
            'total_cases': qs.count(),
            'by_status': dict(qs.values('status').annotate(count=Count('id')).values_list('status', 'count')),
            'by_priority': dict(qs.values('priority').annotate(count=Count('id')).values_list('priority', 'count')),
            'recent_cases': BiopiracyCaseSerializer(qs.order_by('-detected_date')[:10], many=True).data,
            'assigned_to_me': qs.filter(assigned_to=request.user, status__in=['DETECTED', 'UNDER_REVIEW', 'ESCALATED']).count(),
        }
        return Response(summary)


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['type', 'severity', 'is_read', 'is_action_required']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        alert = self.get_object()
        alert.is_read = True
        alert.save()
        return Response({'message': 'Marked as read'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        Alert.objects.filter(is_read=False).update(is_read=True)
        return Response({'message': 'All alerts marked as read'})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = Alert.objects.filter(is_read=False).count()
        return Response({'unread_count': count})

    @action(detail=False, methods=['get'])
    def recent(self, request):
        alerts = self.get_queryset()[:20]
        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data)


class TKDL_EntryViewSet(viewsets.ModelViewSet):
    queryset = TKDL_Entry.objects.select_related('formulation').all()
    serializer_class = TKDL_EntrySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filterset_fields = ['ayush_category', 'is_verified', 'digitized_date']
    search_fields = ['formulation_name', 'text_source', 'notes']

    @action(detail=False, methods=['get'])
    def coverage_stats(self, request):
        total = TKDL_Entry.objects.count()
        verified = TKDL_Entry.objects.filter(is_verified=True).count()
        by_category = dict(TKDL_Entry.objects.values('ayush_category').annotate(count=Count('id')).values_list('ayush_category', 'count'))

        return Response({
            'total_entries': total,
            'verified': verified,
            'verification_rate': round((verified / total * 100) if total > 0 else 0, 2),
            'by_category': by_category,
            'overall_coverage': round((TKDL_Entry.objects.filter(coverage_percentage__gt=0).aggregate(avg=Avg('coverage_percentage'))['avg'] or 0), 2),
        })


class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def kpis(self, request):
        today = timezone.now().date()
        stat, _ = DashboardStat.objects.get_or_create(date=today)

        kpis = {
            'total_gi_tags': GITag.objects.count(),
            'total_patents': Patent.objects.count(),
            'total_biopiracy_alerts': Alert.objects.filter(type='BIOPIRACY').count(),
            'active_biopiracy_cases': BiopiracyCase.objects.filter(
                status__in=['DETECTED', 'UNDER_REVIEW', 'ESCALATED']
            ).count(),
            'resolved_biopiracy_cases': BiopiracyCase.objects.filter(status='RESOLVED').count(),
            'texts_digitized': TKDL_Entry.objects.filter(digitized_date__isnull=False).count(),
            'total_formulations': AYUSHFormulation.objects.count(),
            'registered_formulations': AYUSHFormulation.objects.filter(is_registered=True).count(),
            'india_prior_art_success': BiopiracyCase.objects.filter(prior_art_submitted=True).count(),
            'monthly_trends': self._get_monthly_trends(),
            'category_distribution': self._get_category_distribution(),
            'state_wise_data': self._get_state_wise_data(),
            'recent_alerts': AlertSerializer(Alert.objects.order_by('-created_at')[:5], many=True).data,
            'recent_activities': IPActivitySerializer(IPActivity.objects.order_by('-created_at')[:10], many=True).data,
        }
        return Response(kpis)

    def _get_monthly_trends(self):
        trends = {}
        for i in range(12):
            month_start = timezone.now().date().replace(day=1) - timedelta(days=30 * i)
            month_end = month_start + timedelta(days=30)
            month_key = month_start.strftime('%Y-%m')
            trends[month_key] = {
                'gi_tags': GITag.objects.filter(issued_date__range=[month_start, month_end]).count(),
                'patents': Patent.objects.filter(filing_date__range=[month_start, month_end]).count(),
                'biopiracy_cases': BiopiracyCase.objects.filter(detected_date__date__range=[month_start, month_end]).count(),
            }
        return dict(sorted(trends.items()))

    def _get_category_distribution(self):
        return {
            cat: {
                'gi_tags': GITag.objects.filter(category=cat).count(),
                'patents': Patent.objects.filter(ayush_category=cat).count(),
                'formulations': AYUSHFormulation.objects.filter(category=cat).count(),
            }
            for cat, _ in AYUSHCategory.choices
        }

    def _get_state_wise_data(self):
        states = State.objects.filter(is_active=True)
        result = []
        for state in states:
            result.append({
                'state_id': str(state.id),
                'state_name': state.name,
                'state_code': state.code,
                'latitude': state.latitude,
                'longitude': state.longitude,
                'gi_tags': GITag.objects.filter(state=state).count(),
                'patents': 0,
                'formulations': AYUSHFormulation.objects.filter(state_of_origin=state).count(),
                'biopiracy_cases': BiopiracyCase.objects.filter(
                    patent__in=Patent.objects.filter(country='IN')
                ).count(),
            })
        return result

    @action(detail=False, methods=['get'])
    def state_analytics(self, request):
        state_id = request.query_params.get('state_id')
        if not state_id:
            return Response({'error': 'state_id required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            state = State.objects.get(id=state_id)
        except State.DoesNotExist:
            return Response({'error': 'State not found'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'state': StateSerializer(state).data,
            'gi_tags': GITag.objects.filter(state=state).count(),
            'patents': Patent.objects.filter(assignee__icontains=state.name).count() if hasattr(Patent, 'assignee') else 0,
            'formulations': AYUSHFormulation.objects.filter(state_of_origin=state).count(),
            'biopiracy_cases': BiopiracyCase.objects.filter(
                formulation__state_of_origin=state
            ).count(),
            'tkdl_coverage': TKDL_Entry.objects.filter(
                formulation__state_of_origin=state
            ).aggregate(avg=Avg('coverage_percentage'))['avg'] or 0,
        }
        return Response(data)

    @action(detail=False, methods=['post'])
    def compare_states(self, request):
        serializer = ComparisonRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        state_ids = serializer.validated_data['state_ids']

        states = State.objects.filter(id__in=state_ids)
        comparison = []
        for state in states:
            comparison.append({
                'state': StateSerializer(state).data,
                'gi_tags': GITag.objects.filter(state=state).count(),
                'patents': Patent.objects.filter(assignee__icontains=state.name).count(),
                'formulations': AYUSHFormulation.objects.filter(state_of_origin=state).count(),
                'biopiracy_cases': BiopiracyCase.objects.filter(
                    formulation__state_of_origin=state
                ).count(),
                'tkdl_coverage': TKDL_Entry.objects.filter(
                    formulation__state_of_origin=state
                ).aggregate(avg=Avg('coverage_percentage'))['avg'] or 0,
            })
        return Response(comparison)


class IPActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IPActivity.objects.select_related('related_state', 'related_user').all()
    serializer_class = IPActivitySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['activity_type']
    ordering = ['-created_at']


class CaseTrackerViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def table_data(self, request):
        state = request.query_params.get('state')
        status_filter = request.query_params.get('status')
        case_type = request.query_params.get('type')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        cases = BiopiracyCase.objects.select_related('patent', 'formulation', 'assigned_to').all()

        if state:
            cases = cases.filter(formulation__state_of_origin_id=state)
        if status_filter:
            cases = cases.filter(status=status_filter)
        if case_type:
            cases = cases.filter(detection_method=case_type)
        if date_from:
            cases = cases.filter(detected_date__date__gte=date_from)
        if date_to:
            cases = cases.filter(detected_date__date__lte=date_to)

        serializer = BiopiracyCaseSerializer(cases[:100], many=True)
        return Response(serializer.data)


def api_index(request):
    """Simple HTML landing page at the server root so '/ ' is not a 404."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>IP-SAKTI API — Ministry of Ayush</title>
    <style>
        body { font-family: 'Segoe UI', system-ui, sans-serif; max-width: 760px; margin: 60px auto; padding: 0 24px; color: #1a202c; background: #f7fafc; }
        h1 { color: #2b6cb0; margin-bottom: 4px; }
        .sub { color: #4a5568; margin-bottom: 32px; }
        code { background: #edf2f7; padding: 2px 6px; border-radius: 4px; font-size: 0.92em; }
        li { margin: 6px 0; }
        .card { background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 24px 28px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
        a { color: #2b6cb0; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .btn { display: inline-block; margin-top: 20px; padding: 10px 18px; background: #2b6cb0; color: white !important; border-radius: 6px; }
        .btn:hover { background: #2c5282; text-decoration: none !important; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🛡️ IP-SAKTI API</h1>
        <p class="sub">Biopiracy-tracking portal for India's AYUSH traditional knowledge — Ministry of Ayush (SIH 2026)</p>
        <p>This is the <strong>backend API server</strong>. The dashboard UI runs separately on the Vite dev server:</p>
        <a class="btn" href="http://localhost:5173">Open Dashboard UI → http://localhost:5173</a>
        <p style="margin-top: 28px; margin-bottom: 8px;"><strong>Available endpoints</strong></p>
        <ul>
            <li><code>POST /api/auth/token/</code> — obtain JWT (username + password)</li>
            <li><code>POST /api/auth/token/refresh/</code> — refresh access token</li>
            <li><code>/api/users/</code> — user accounts &amp; profile (<code>me/</code>, <code>register/</code>)</li>
            <li><code>/api/</code> — core resources: states, formulations, gi-tags, patents, biopiracy-cases, tkdl, activities, compare-states…</li>
            <li><code>/api/dashboard/</code> — kpis, summary, monthly-trends, state-analytics</li>
            <li><code>/api/alerts/</code> — alert feed + case-tracker</li>
            <li><code>/admin/</code> — Django admin</li>
        </ul>
        <p style="margin-top: 24px; color: #4a5568;">All resource endpoints require a JWT <code>Authorization: Bearer &lt;access&gt;</code> header. Demo logins are in <code>README.md</code>.</p>
    </div>
</body>
</html>"""
    return HttpResponse(html)
