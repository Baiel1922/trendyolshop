from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
class IsActivePermission(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)

class IsAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user == obj.user
        )
