from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from ip_sakti.models import User
from ip_sakti.serializers import UserSerializer, UserCreateSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'ADMIN'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        # Regular users may only see/edit themselves; admins see everyone.
        user = self.request.user
        if user.is_authenticated and (user.role == 'ADMIN' or user.is_superuser):
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'me', 'switch_language']:
            return [permissions.IsAuthenticated()]
        return [IsAdminOrReadOnly()]

    def update(self, request, *args, **kwargs):
        # Restrict self-service profile edits to safe fields.
        allowed = {'first_name', 'last_name', 'phone', 'designation',
                   'preferred_language', 'ministry_department'}
        data = {k: v for k, v in request.data.items() if k in allowed}
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get', 'patch', 'put'])
    def me(self, request):
        if request.method in ('PATCH', 'PUT'):
            allowed = {'first_name', 'last_name', 'phone', 'designation',
                       'preferred_language', 'ministry_department'}
            data = {k: v for k, v in request.data.items() if k in allowed}
            serializer = self.get_serializer(request.user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
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
