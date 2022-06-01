from rest_framework import permissions

class IsCurrentUser(permissions.BasePermission):
    message = "You are not allowed to update others profiles"

    def has_object_permission(self, request, view, obj):
        if request.user.username == obj.username:
            return True
        return False