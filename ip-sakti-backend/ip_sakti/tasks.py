from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import requests
import json
from .models import Patent, BiopiracyCase, Alert, DashboardStat, TKDL_Entry, IPActivity, AYUSHFormulation, GITag, BiopiracyCaseStatus, AYUSHCategory


@shared_task
def fetch_patent_data():
    try:
        response = requests.get(
            f"{settings.IP_INDIA_API_URL}/api/patents/recent",
            timeout=30,
            params={'days': 7, 'category': 'AYUSH'}
        )
        if response.status_code == 200:
            data = response.json()
            for patent_data in data.get('patents', []):
                Patent.objects.get_or_create(
                    application_number=patent_data['application_number'],
                    defaults={
                        'title': patent_data['title'],
                        'applicant': patent_data['applicant'],
                        'country': patent_data.get('country', 'IN'),
                        'filing_date': patent_data['filing_date'],
                        'status': patent_data.get('status', 'FILED'),
                        'ayush_category': patent_data.get('category', 'AYURVEDA'),
                        'abstract': patent_data.get('abstract', ''),
                    }
                )
        IPActivity.objects.create(
            activity_type='PATENT_FILED',
            title='Patent data fetched',
            description='Scheduled patent data fetch completed successfully',
        )
    except Exception as e:
        IPActivity.objects.create(
            activity_type='SYSTEM',
            title='Patent fetch failed',
            description=str(e),
        )


@shared_task
def detect_biopiracy_candidates():
    recent_patents = Patent.objects.filter(
        is_biopiracy_suspect=False,
        filing_date__gte=timezone.now().date() - timedelta(days=30)
    )

    for patent in recent_patents:
        risk_score = 0
        risk_factors = []

        formulations = AYUSHFormulation.objects.filter(
            name__icontains=patent.title.split()[0] if patent.title else ''
        )
        if formulations.exists():
            risk_score += 40
            risk_factors.append('Formulation name match')

        if patent.applicant and patent.applicant not in ['CSIR', 'IP India', 'Ministry of AYUSH']:
            if not patent.applicant.startswith('Indian'):
                risk_score += 20
                risk_factors.append('Non-Indian applicant')

        if patent.ayush_category in ['AYURVEDA', 'SIDDHA', 'UNANI']:
            risk_score += 15
            risk_factors.append('High-risk AYUSH category')

        if not patent.is_biopiracy_suspect and risk_score >= 50:
            patent.is_biopiracy_suspect = True
            patent.biopiracy_risk_score = min(risk_score, 100)
            patent.save()

            case = BiopiracyCase.objects.create(
                patent=patent,
                formulation=formulations.first() if formulations.exists() else None,
                risk_score=min(risk_score, 100),
                description=f"Automated detection: {'; '.join(risk_factors)}",
            )

            alert = Alert.objects.create(
                type='BIOPIRACY',
                severity='HIGH' if risk_score > 70 else 'MEDIUM',
                title=f"Potential Biopiracy: {patent.title[:80]}",
                message=f"Suspicious patent filing detected. Risk score: {risk_score}. Risk factors: {'; '.join(risk_factors)}",
                related_case=case,
                is_action_required=True,
            )
            IPActivity.objects.create(
                activity_type='BIOPIRACY_DETECTED',
                title=f'Biopiracy candidate detected: {patent.title[:50]}',
                description=f'Risk score: {risk_score}',
                metadata={'case_id': str(case.id), 'patent_id': str(patent.id)}
            )


@shared_task
def generate_daily_stats():
    today = timezone.now().date()
    stats = {
        'date': today,
        'total_gi_tags': GITag.objects.count(),
        'total_patents': Patent.objects.count(),
        'total_biopiracy_cases': BiopiracyCase.objects.count(),
        'active_biopiracy_cases': BiopiracyCase.objects.filter(
            status__in=['DETECTED', 'UNDER_REVIEW', 'ESCALATED']
        ).count(),
        'resolved_biopiracy_cases': BiopiracyCase.objects.filter(status='RESOLVED').count(),
        'total_formulations': AYUSHFormulation.objects.count(),
        'digitized_formulations': AYUSHFormulation.objects.filter(digitized_in_tkdl=True).count(),
        'total_alerts': Alert.objects.count(),
        'unread_alerts': Alert.objects.filter(is_read=False).count(),
        'state_wise_gi': {},
        'state_wise_patents': {},
        'category_distribution': {},
        'monthly_trends': {},
    }

    from .views import DashboardViewSet
    viewset = DashboardViewSet()
    stats['monthly_trends'] = viewset._get_monthly_trends()
    stats['category_distribution'] = viewset._get_category_distribution()
    stats['state_wise_gi'] = viewset._get_state_wise_data()

    DashboardStat.objects.update_or_create(date=today, defaults=stats)


@shared_task
def send_alert_notifications():
    unread_alerts = Alert.objects.filter(
        notification_sent_email=False,
        severity__in=['HIGH', 'CRITICAL']
    )
    for alert in unread_alerts:
        alert.notification_sent_email = True
        alert.save()


@shared_task
def clean_old_alerts():
    expiry_date = timezone.now() - timedelta(days=90)
    Alert.objects.filter(created_at__lt=expiry_date, is_read=True).delete()


@shared_task
def update_tkdl_coverage():
    entries = TKDL_Entry.objects.filter(coverage_percentage__lt=100)
    for entry in entries:
        if entry.total_texts > 0:
            entry.coverage_percentage = min(
                (entry.digitized_texts / entry.total_texts) * 100,
                100
            )
            entry.save()


@shared_task
def simulate_realtime_alert():
    import random
    patents = list(Patent.objects.all()[:50])
    if not patents:
        return
    patent = random.choice(patents)
    case = BiopiracyCase.objects.create(
        patent=patent,
        risk_score=random.randint(50, 95),
        description="Simulated biopiracy detection for demonstration purposes",
    )
    Alert.objects.create(
        type='BIOPIRACY',
        severity=random.choice(['HIGH', 'CRITICAL']),
        title=f"LIVE: Biopiracy Alert - {patent.title[:60]}",
        message=f"New biopiracy attempt detected from {patent.country}. Risk score: {case.risk_score}",
        related_case=case,
        is_action_required=True,
    )
    return str(case.id)
