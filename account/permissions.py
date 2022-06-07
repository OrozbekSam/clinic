from rest_framework.permissions import BasePermission, SAFE_METHODS

from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if view.name == 'Add to liked':
            return request.user.is_active
        if view.name == 'Remove from liked':
            return request.user.is_active
        return obj.owner == request.user
    
    
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_staff