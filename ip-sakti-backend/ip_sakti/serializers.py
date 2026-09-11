from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    State, AYUSHFormulation, GITag, Patent, BiopiracyCase,
    Alert, TKDL_Entry, DashboardStat, IPActivity
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'username', 'role', 'ministry_department', 'phone', 'designation',
            'is_verified', 'preferred_language', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'username',
            'password', 'role', 'ministry_department', 'phone', 'designation'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class StateSerializer(serializers.ModelSerializer):
    gi_tags_count = serializers.SerializerMethodField()
    patents_count = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = [
            'id', 'name', 'code', 'region', 'ayush_council_name',
            'population', 'gdp_contribution', 'latitude', 'longitude',
            'is_active', 'gi_tags_count', 'patents_count', 'created_at'
        ]

    def get_gi_tags_count(self, obj):
        return obj.gi_tags.filter(is_ayush_related=True).count()

    def get_patents_count(self, obj):
        return 0


class AYUSHFormulationSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state_of_origin.name', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = AYUSHFormulation
        fields = [
            'id', 'name', 'sanskrit_name', 'ingredients', 'preparation_method',
            'source_text', 'text_reference', 'category', 'indication',
            'therapeutic_uses', 'is_registered', 'registration_number',
            'state_of_origin', 'state_name', 'traditional_knowledge_holders',
            'documentation_date', 'digitized_in_tkdl', 'tkdl_entry_date',
            'category_display', 'created_at', 'updated_at'
        ]


class GITagSerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    state_code = serializers.CharField(source='state.code', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = GITag
        fields = [
            'id', 'name', 'product', 'description', 'state', 'state_name', 'state_code',
            'category', 'category_display', 'status', 'status_display',
            'issued_date', 'expiry_date', 'applicant', 'registration_number',
            'geographical_area', 'is_ayush_related', 'created_at', 'updated_at'
        ]


class PatentSerializer(serializers.ModelSerializer):
    ayush_category_display = serializers.CharField(source='get_ayush_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Patent
        fields = [
            'id', 'title', 'applicant', 'country', 'application_number',
            'publication_number', 'patent_number', 'filing_date',
            'publication_date', 'grant_date', 'status', 'status_display',
            'ayush_category', 'ayush_category_display', 'abstract',
            'claims_summary', 'is_biopiracy_suspect', 'biopiracy_risk_score',
            'ipc_codes', 'assignee', 'inventors', 'data_source',
            'fetched_at', 'created_at', 'updated_at'
        ]


class BiopiracyCaseSerializer(serializers.ModelSerializer):
    patent_title = serializers.CharField(source='patent.title', read_only=True)
    formulation_name = serializers.CharField(source='formulation.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)

    class Meta:
        model = BiopiracyCase
        fields = [
            'id', 'patent', 'patent_title', 'formulation', 'formulation_name',
            'status', 'status_display', 'priority', 'priority_display',
            'detected_date', 'detection_method', 'risk_score', 'description',
            'assigned_to', 'assigned_to_name', 'resolution_notes',
            'resolved_date', 'prior_art_submitted', 'prior_art_date',
            'country_of_origin', 'notification_sent', 'created_at', 'updated_at'
        ]


class AlertSerializer(serializers.ModelSerializer):
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    related_case_id = serializers.UUIDField(source='related_case.id', read_only=True)

    class Meta:
        model = Alert
        fields = [
            'id', 'type', 'type_display', 'severity', 'severity_display',
            'title', 'message', 'related_case', 'related_case_id',
            'related_gi_tag', 'related_patent', 'is_read', 'is_action_required',
            'action_taken_by', 'action_taken_at', 'notification_sent_email',
            'notification_sent_sms', 'created_at', 'expires_at'
        ]


class TKDL_EntrySerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_ayush_category_display', read_only=True)
    verified_by_name = serializers.CharField(source='verified_by.get_full_name', read_only=True)

    class Meta:
        model = TKDL_Entry
        fields = [
            'id', 'formulation_name', 'text_source', 'text_source_language',
            'digitized_date', 'coverage_percentage', 'total_texts',
            'digitized_texts', 'formulation', 'ayush_category', 'category_display',
            'is_verified', 'verified_by', 'verified_by_name', 'notes',
            'created_at', 'updated_at'
        ]


class DashboardStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardStat
        fields = [
            'id', 'date', 'total_gi_tags', 'total_patents',
            'total_biopiracy_cases', 'active_biopiracy_cases',
            'resolved_biopiracy_cases', 'total_formulations',
            'digitized_formulations', 'total_alerts', 'unread_alerts',
            'state_wise_gi', 'state_wise_patents', 'category_distribution',
            'monthly_trends', 'created_at'
        ]


class IPActivitySerializer(serializers.ModelSerializer):
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)
    related_state_name = serializers.CharField(source='related_state.name', read_only=True)

    class Meta:
        model = IPActivity
        fields = [
            'id', 'activity_type', 'activity_type_display', 'title',
            'description', 'related_state', 'related_state_name',
            'related_user', 'metadata', 'created_at'
        ]


class KPIResponseSerializer(serializers.Serializer):
    total_gi_tags = serializers.IntegerField()
    total_patents = serializers.IntegerField()
    total_biopiracy_alerts = serializers.IntegerField()
    active_biopiracy_cases = serializers.IntegerField()
    resolved_biopiracy_cases = serializers.IntegerField()
    texts_digitized = serializers.IntegerField()
    total_formulations = serializers.IntegerField()
    registered_formulations = serializers.IntegerField()
    india_prior_art_success = serializers.IntegerField(help_text='India First counter - prior art wins')
    monthly_trends = serializers.DictField()
    category_distribution = serializers.DictField()


class StateAnalyticsSerializer(serializers.Serializer):
    state = StateSerializer()
    gi_tags = serializers.IntegerField()
    patents = serializers.IntegerField()
    formulations = serializers.IntegerField()
    biopiracy_cases = serializers.IntegerField()
    tkdl_coverage = serializers.DecimalField(max_digits=5, decimal_places=2)


class ComparisonRequestSerializer(serializers.Serializer):
    state_ids = serializers.ListField(child=serializers.UUIDField(), min_length=2, max_length=4)
    metrics = serializers.ListField(child=serializers.CharField(), default=['gi_tags', 'patents', 'formulations'])
