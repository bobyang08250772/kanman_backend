from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import NotFound
from dashboard_app.models import Task



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

    """Grant at the view level"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Grant if user is task assignee or superuser."""
        user = request.user
        return (
            user and user.is_authenticated and (
                user == obj.assignee or
                user.is_superuser
            )
        )
    

class IsAuthenticatedAndBoardMember(BasePermission):
    """Allow if user is board member or  superuser."""
   
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user in obj.board.members.all()


class IsAuthenticatedAndRevieingOrSuperUser(BasePermission):
    """Allow if user is assginee or is superuser."""

    """Grant at the view level"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

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
    def has_permission(self, request, view):
        task_id = view.kwargs.get('task_id')
    
        try:
            task = Task.objects.select_related('board').get(id=task_id)
        except Task.DoesNotExist:
            raise NotFound("Task not found.")
        
        user = request.user
        return user.is_superuser or user in task.board.members.all()


    def has_object_permission(self, request, view, obj):
        """Grant if user is task assignee, creator, reviewer, or superuser."""
        user = request.user
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
        
