from django.db import models
from rest_framework import permissions


class AbstractTimestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NonSecurePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return False
        else:
            return True
