from rest_framework import permissions


class IsManeger(permissions.BasePermission):

    def has_permission(self, request, view):
        # check user is auttenticated and manager
        return  request.user.is_authenticated and (request.user.user_type==1)

    def has_object_permission(self, request, view, obj):
        # check user is auttenticated and manager
        return  request.user.is_authenticated and (request.user.user_type==1)

class IsPersonnel(permissions.BasePermission):

    def has_permission(self, request, view):
        # check user is auttenticated and manager
        return  request.user.is_authenticated and (request.user.user_type<=2)

    def has_object_permission(self, request, view, obj):
        # check user is auttenticated and manager
        return  request.user.is_authenticated and (request.user.user_type<=2)