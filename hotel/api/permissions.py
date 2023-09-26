from rest_framework import permissions

class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff
    
class IsReservationOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(f"request.user: {request.user}")
        print(f"obj.host: {obj.host}")
        return request.user == obj.host
