from rest_framework.permissions import BasePermission


class IsAuthorPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return request.user.is_authenticated and request.user == obj.author
