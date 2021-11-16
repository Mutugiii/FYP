from rest_framework.permissions import BasePermission

class IsAuthenticatedClient(BasePermission):
    def has_permission(self, request, view):
        '''
        Allow authenticated user requests
        '''        
        return request.user and request.user.is_authenticated


class IsAuthenticatedStaff(BasePermission):
    def has_permission(self, request, view):
        '''
        Allow authenticated staff requests
        '''        
        return request.user and request.user.is_staff


class IsAuthenticatedClientOrStaff(BasePermission):
    def has_permission(self, request, view):
        '''
        Allow authenticated staff requests
        '''        
        return (request.user and request.user.is_staff) or (request.user and request.user.is_authenticated)