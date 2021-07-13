from rest_framework import permissions


class AccessPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user or request.user.is_superuser
