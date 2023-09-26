from rest_framework import permissions

class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff
    
class IsReservationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.host
