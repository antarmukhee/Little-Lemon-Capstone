from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsManager(BasePermission):
    """
    Allows access only to manager users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.groups.filter(name = 'Manager'))
    
class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        is_manager = bool(request.user.groups.filter(name = 'Manager'))
        is_delivery_crew = bool(request.user.groups.filter(name = 'Delivery crew'))
        is_customer = not (is_manager or is_delivery_crew)
        return bool(request.user and request.user.is_authenticated and is_customer)

class IsAuthenticatedAndReadOnly(BasePermission):
    """
    Allows access to authenticated users only if the request is read-only
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS and
            request.user and
            request.user.is_authenticated
        )