# Serializers for the users app. The canonical definitions live in
# ip_sakti.serializers; re-export them so `from .serializers import ...`
# in users/views.py works.
from ip_sakti.serializers import UserSerializer, UserCreateSerializer  # noqa: F401

__all__ = ['UserSerializer', 'UserCreateSerializer']
