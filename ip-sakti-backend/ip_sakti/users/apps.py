from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ip_sakti.users'
    label = 'users'

    def ready(self):
        # The User model is defined in ip_sakti.models; import it here so the
        # app registry picks it up under the 'users' label.
        from . import models  # noqa: F401
