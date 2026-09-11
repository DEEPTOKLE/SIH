import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Canonical User model for IP-SAKTI (AUTH_USER_MODEL = 'users.User')."""

    ROLE_CHOICES = (
        ('ADMIN', _('Administrator')),
        ('MINISTRY', _('Ministry Official')),
        ('ANALYST', _('Analyst')),
        ('VIEWER', _('Viewer')),
    )
    DEPARTMENT_CHOICES = (
        ('AYUSH', _('AYUSH')),
        ('CSIR', _('CSIR')),
        ('IPINDIA', _('IP India')),
        ('TKDL', _('TKDL')),
        ('GIPD', _('GI Registry')),
        ('OTHER', _('Other')),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='VIEWER')
    ministry_department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='AYUSH')
    phone = models.CharField(max_length=15, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    digilocker_id = models.CharField(max_length=100, blank=True)
    preferred_language = models.CharField(max_length=5, default='en')
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    def is_admin(self):
        return self.role == 'ADMIN'

    def is_ministry_official(self):
        return self.role == 'MINISTRY'

    def can_edit(self):
        return self.role in ['ADMIN', 'MINISTRY', 'ANALYST']
