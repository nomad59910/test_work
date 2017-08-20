from rest_framework import permissions


class IsAddedAuthorizedUser(permissions.BasePermission):
    message = 'Вы не можете изменять эту задачу.'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user_added
