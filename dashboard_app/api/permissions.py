from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticateAndNotGuestUser(BasePermission):
    """Allow only authenticated users; deny guest user for write operations."""

    def has_permission(self, request, view):
        """Grant if user is authenticated (and not guest for write)."""
        user = request.user
        if request.method in SAFE_METHODS:
            return user.is_authenticated
        return user.is_authenticated and user.email.lower() != 'guest@guest.de'
    

class IsAuthenticatedAndBoardRelatedOrSuperUser(BasePermission):
    """Allow if user is related to the board or is superuser."""

    def has_object_permission(self, request, view, obj):
        """Grant if user is board member or owner or superuser."""
        user = request.user
        if request.method in SAFE_METHODS:
            return user and user.is_authenticated
        return (
            user and user.is_authenticated and (
                user == obj.owner or
                obj.members.filter(id=user.id).exists() or
                user.is_superuser
            )
        )
        

class IsAuthenticatedAndTAssignToMeOrSuperUser(BasePermission):
    """Allow if user is assginee or is superuser."""

    def has_object_permission(self, request, view, obj):
        """Grant if user is task assignee or superuser."""
        user = request.user
        return (
            user and user.is_authenticated and (
                user == obj.assignee or
                user.is_superuser
            )
        )
    

class IsAuthenticatedAndRevieingOrSuperUser(BasePermission):
    """Allow if user is assginee or is superuser."""

    def has_object_permission(self, request, view, obj):
        """Grant if user is task assignee or superuser."""
        user = request.user
        return (
            user and user.is_authenticated and (
                user == obj.reviewer or
                user.is_superuser
            )
        )


class IsAuthenticatedAndTaskRelatedOrSuperUser(BasePermission):
    """Allow if user is related to the task or is superuser."""

    def has_object_permission(self, request, view, obj):
        """Grant if user is task assignee, creator, reviewer, or superuser."""
        user = request.user
        if request.method in SAFE_METHODS:
            return user and user.is_authenticated
        return (
            user and user.is_authenticated and (
                user == obj.assignee or
                user == obj.creator or
                user == obj.reviewer or
                user.is_superuser
            )
        )
    
class IsAuthenticatedAndSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method == 'DELETE':
            return user and user.is_authenticated and user == obj.user
        
