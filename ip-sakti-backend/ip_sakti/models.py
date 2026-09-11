import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

# The User model is canonically defined in ip_sakti.users.models
# (AUTH_USER_MODEL = 'users.User'); re-exported here so existing imports of
# `from ip_sakti.models import User` keep working.
from ip_sakti.users.models import User  # noqa: F401


class Region(models.TextChoices):
    NORTH = 'NORTH', _('North')
    SOUTH = 'SOUTH', _('South')
    EAST = 'EAST', _('East')
    WEST = 'WEST', _('West')
    CENTRAL = 'CENTRAL', _('Central')
    NORTHEAST = 'NORTHEAST', _('Northeast')
    UNION_TERRITORY = 'UT', _('Union Territory')


class State(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)
    region = models.CharField(max_length=20, choices=Region.choices)
    ayush_council_name = models.CharField(max_length=200, blank=True)
    population = models.BigIntegerField(default=0)
    gdp_contribution = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'State'
        verbose_name_plural = 'States'

    def __str__(self):
        return self.name


class AYUSHCategory(models.TextChoices):
    AYURVEDA = 'AYURVEDA', _('Ayurveda')
    YOGA = 'YOGA', _('Yoga & Naturopathy')
    UNANI = 'UNANI', _('Unani')
    SIDDHA = 'SIDDHA', _('Siddha')
    HOMOEOPATHY = 'HOMOEOPATHY', _('Homoeopathy')
    SOWRIGANDHA = 'SOWRIGANDHA', _('Sowrighandha / Traditional')


class GITagStatus(models.TextChoices):
    REGISTERED = 'REGISTERED', _('Registered')
    PENDING = 'PENDING', _('Pending')
    EXAMINED = 'EXAMINED', _('Examined')
    REJECTED = 'REJECTED', _('Rejected')
    EXPIRED = 'EXPIRED', _('Expired')


class GITag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='gi_tags')
    category = models.CharField(max_length=20, choices=AYUSHCategory.choices, default=AYUSHCategory.AYURVEDA)
    status = models.CharField(max_length=20, choices=GITagStatus.choices, default=GITagStatus.PENDING)
    issued_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    applicant = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100, unique=True)
    geographical_area = models.CharField(max_length=255, blank=True)
    is_ayush_related = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-issued_date']
        verbose_name = 'GI Tag'
        verbose_name_plural = 'GI Tags'

    def __str__(self):
        return f"{self.name} ({self.product}) - {self.state.name}"


class PatentStatus(models.TextChoices):
    FILED = 'FILED', _('Filed')
    PUBLISHED = 'PUBLISHED', _('Published')
    EXAMINED = 'EXAMINED', _('Examined')
    GRANTED = 'GRANTED', _('Granted')
    REJECTED = 'REJECTED', _('Rejected')
    ABANDONED = 'ABANDONED', _('Abandoned')
    EXPIRED = 'EXPIRED', _('Expired')


class Patent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    applicant = models.CharField(max_length=255)
    country = models.CharField(max_length=100, default='IN')
    application_number = models.CharField(max_length=100, unique=True)
    publication_number = models.CharField(max_length=100, blank=True)
    patent_number = models.CharField(max_length=100, blank=True)
    filing_date = models.DateField()
    publication_date = models.DateField(null=True, blank=True)
    grant_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=PatentStatus.choices, default=PatentStatus.FILED)
    ayush_category = models.CharField(max_length=20, choices=AYUSHCategory.choices, default=AYUSHCategory.AYURVEDA)
    abstract = models.TextField(blank=True)
    claims_summary = models.TextField(blank=True)
    is_biopiracy_suspect = models.BooleanField(default=False)
    biopiracy_risk_score = models.IntegerField(default=0, help_text='0-100 risk score')
    ipc_codes = models.CharField(max_length=255, blank=True, help_text='IPC classification codes')
    assignee = models.CharField(max_length=255, blank=True)
    inventors = models.CharField(max_length=500, blank=True)
    data_source = models.CharField(max_length=100, default='IP_INDIA')
    fetched_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-filing_date']
        verbose_name = 'Patent'
        verbose_name_plural = 'Patents'

    def __str__(self):
        return f"{self.title} ({self.applicant})"


class BiopiracyCaseStatus(models.TextChoices):
    DETECTED = 'DETECTED', _('Detected')
    UNDER_REVIEW = 'UNDER_REVIEW', _('Under Review')
    ESCALATED = 'ESCALATED', _('Escalated')
    PRIOR_ART_FILED = 'PRIOR_ART_FILED', _('Prior Art Filed')
    RESOLVED = 'RESOLVED', _('Resolved')
    FALSE_POSITIVE = 'FALSE_POSITIVE', _('False Positive')
    CLOSED = 'CLOSED', _('Closed')


class BiopiracyCase(models.Model):
    PRIORITY_CHOICES = (
        ('LOW', _('Low')),
        ('MEDIUM', _('Medium')),
        ('HIGH', _('High')),
        ('CRITICAL', _('Critical')),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patent = models.ForeignKey(Patent, on_delete=models.CASCADE, related_name='biopiracy_cases')
    formulation = models.ForeignKey('AYUSHFormulation', on_delete=models.SET_NULL, null=True, related_name='biopiracy_cases')
    status = models.CharField(max_length=20, choices=BiopiracyCaseStatus.choices, default=BiopiracyCaseStatus.DETECTED)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    detected_date = models.DateTimeField(auto_now_add=True)
    detection_method = models.CharField(max_length=100, default='RULE_BASED')
    risk_score = models.IntegerField(default=0)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_biopiracy_cases')
    resolution_notes = models.TextField(blank=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    prior_art_submitted = models.BooleanField(default=False)
    prior_art_date = models.DateTimeField(null=True, blank=True)
    country_of_origin = models.CharField(max_length=100, blank=True)
    notification_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-detected_date']
        verbose_name = 'Biopiracy Case'
        verbose_name_plural = 'Biopiracy Cases'

    def __str__(self):
        return f"Biopiracy: {self.patent.title[:50]}"


class AYUSHFormulation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    sanskrit_name = models.CharField(max_length=255, blank=True)
    ingredients = models.JSONField(default=list, help_text='List of ingredients with quantities')
    preparation_method = models.TextField(blank=True)
    source_text = models.CharField(max_length=255, blank=True)
    text_reference = models.CharField(max_length=500, blank=True)
    category = models.CharField(max_length=20, choices=AYUSHCategory.choices)
    indication = models.CharField(max_length=255, blank=True)
    therapeutic_uses = models.TextField(blank=True)
    is_registered = models.BooleanField(default=False)
    registration_number = models.CharField(max_length=100, blank=True)
    state_of_origin = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, related_name='formulations')
    traditional_knowledge_holders = models.CharField(max_length=255, blank=True)
    documentation_date = models.DateField(null=True, blank=True)
    digitized_in_tkdl = models.BooleanField(default=False)
    tkdl_entry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'AYUSH Formulation'
        verbose_name_plural = 'AYUSH Formulations'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['is_registered']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class AlertSeverity(models.TextChoices):
    INFO = 'INFO', _('Information')
    LOW = 'LOW', _('Low')
    MEDIUM = 'MEDIUM', _('Medium')
    HIGH = 'HIGH', _('High')
    CRITICAL = 'CRITICAL', _('Critical')


class AlertType(models.TextChoices):
    BIOPIRACY = 'BIOPIRACY', _('Biopiracy Alert')
    PATENT = 'PATENT', _('Patent Alert')
    GI_TAG = 'GI_TAG', _('GI Tag Alert')
    SYSTEM = 'SYSTEM', _('System Alert')
    TKDL = 'TKDL', _('TKDL Update')
    POLICY = 'POLICY', _('Policy Update')


class Alert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=AlertType.choices)
    severity = models.CharField(max_length=20, choices=AlertSeverity.choices, default=AlertSeverity.INFO)
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_case = models.ForeignKey(BiopiracyCase, on_delete=models.CASCADE, null=True, blank=True, related_name='alerts')
    related_gi_tag = models.ForeignKey(GITag, on_delete=models.CASCADE, null=True, blank=True, related_name='alerts')
    related_patent = models.ForeignKey(Patent, on_delete=models.CASCADE, null=True, blank=True, related_name='alerts')
    is_read = models.BooleanField(default=False)
    is_action_required = models.BooleanField(default=False)
    action_taken_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='actions_taken')
    action_taken_at = models.DateTimeField(null=True, blank=True)
    notification_sent_email = models.BooleanField(default=False)
    notification_sent_sms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'
        indexes = [
            models.Index(fields=['type', 'severity']),
            models.Index(fields=['is_read', 'created_at']),
        ]

    def __str__(self):
        return f"[{self.get_severity_display()}] {self.title}"


class TKDL_Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    formulation_name = models.CharField(max_length=255)
    text_source = models.CharField(max_length=255, help_text='Traditional text reference')
    text_source_language = models.CharField(max_length=50, default='Sanskrit')
    digitized_date = models.DateField(auto_now_add=True)
    coverage_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_texts = models.IntegerField(default=0)
    digitized_texts = models.IntegerField(default=0)
    formulation = models.ForeignKey(AYUSHFormulation, on_delete=models.CASCADE, related_name='tkdl_entries', null=True, blank=True)
    ayush_category = models.CharField(max_length=20, choices=AYUSHCategory.choices, default=AYUSHCategory.AYURVEDA)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_tkdl_entries')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-digitized_date']
        verbose_name = 'TKDL Entry'
        verbose_name_plural = 'TKDL Entries'

    def __str__(self):
        return f"{self.formulation_name} - {self.text_source}"


class DashboardStat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    total_gi_tags = models.IntegerField(default=0)
    total_patents = models.IntegerField(default=0)
    total_biopiracy_cases = models.IntegerField(default=0)
    active_biopiracy_cases = models.IntegerField(default=0)
    resolved_biopiracy_cases = models.IntegerField(default=0)
    total_formulations = models.IntegerField(default=0)
    digitized_formulations = models.IntegerField(default=0)
    total_alerts = models.IntegerField(default=0)
    unread_alerts = models.IntegerField(default=0)
    state_wise_gi = models.JSONField(default=dict, blank=True)
    state_wise_patents = models.JSONField(default=dict, blank=True)
    category_distribution = models.JSONField(default=dict, blank=True)
    monthly_trends = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['date']
        ordering = ['-date']
        verbose_name = 'Dashboard Stat'
        verbose_name_plural = 'Dashboard Stats'

    def __str__(self):
        return f"Stats for {self.date}"


class IPActivity(models.Model):
    ACTIVITY_TYPES = (
        ('GI_ISSUED', _('GI Tag Issued')),
        ('PATENT_FILED', _('Patent Filed')),
        ('PATENT_GRANTED', _('Patent Granted')),
        ('BIOPIRACY_DETECTED', _('Biopiracy Detected')),
        ('BIOPIRACY_RESOLVED', _('Biopiracy Resolved')),
        ('TKDL_ADDED', _('TKDL Entry Added')),
        ('FORMULATION_REGISTERED', _('Formulation Registered')),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    related_state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    related_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'IP Activity'
        verbose_name_plural = 'IP Activities'

    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.title}"
