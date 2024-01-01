from rest_framework.permissions import BasePermission

from users.models import UserRights


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        if request.user.righst == UserRights.MODERATOR:
            return True
        return False


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False
