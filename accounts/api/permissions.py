from rest_framework.permissions import BasePermission

class IsUserVerified(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        print(f'user.is_authenticated: {user.is_authenticated}')
        print(f'user.is_verified: {user.is_verified}')
        return user.is_authenticated and user.is_verified
