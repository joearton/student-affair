from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow the owner of an object to edit it.
    Other users can only read the object (GET).
    """
    
    def has_permission(self, request, view):
        # Allow read-only access (GET, HEAD, OPTIONS) to everyone
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Allow write operations (POST, PUT, DELETE) only for the owner
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # For create operations (POST), allow if the user is authenticated
            if request.method == 'POST':
                return True
            # For update and delete operations, check if the user is the owner
            elif request.method in ['PUT', 'PATCH', 'DELETE']:
                # Assumes the object has an `owner` field that is a ForeignKey to User
                obj = view.get_object()
                return obj.owner == request.user
        return False
