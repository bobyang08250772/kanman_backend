from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated
from dashboard_app.models import Board, Task, Comment
from django.shortcuts import get_object_or_404
from rest_framework import status

from .serializer import BoardSerializer, TaskSerializer, TaskCommentSerializer, BoardListSerializer
from .permissions import IsAuthenticatedAndTaskRelatedOrSuperUser, IsAuthenticateAndNotGuestUser, IsAuthenticatedAndSelf, IsAuthenticatedAndBoardRelatedOrSuperUser, IsAuthenticatedAndTAssignToMeOrSuperUser, IsAuthenticatedAndRevieingOrSuperUser, IsAuthenticatedAndBoardMember, IsAuthenticatedAndCommentRelatedOrSuperUser

class BoardListView(generics.ListCreateAPIView):
    """List all boards or create a new one."""
    permission_classes = [IsAuthenticated]
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a board."""
    permission_classes = [IsAuthenticatedAndBoardRelatedOrSuperUser]
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        owner = instance.owner
        members = instance.members.all()

        return Response({
            'id': instance.id,
            'title': instance.title,
            'owner_data': {
                'id': owner.id,
                'email': owner.email,
                'fullname': f'{owner.first_name} {owner.last_name}'
            }, 
            'members_data':[
                {'id': m.id, 
                 'email': m.email, 
                 'fullname': f'{m.first_name} {m.last_name}'
                 } 
                for m in members]
            }, 
            status=status.HTTP_200_OK)



class TaskListView(generics.ListCreateAPIView):
    """List all tasks or create a new one."""
    permission_classes = [IsAuthenticatedAndBoardMember]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise NotFound(detail="Required fields missing.")  
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        board_id = self.request.data.get('board')
        if not board_id:
            raise NotFound("Board ID is required.")

        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            raise NotFound("Board not found.")

        user = self.request.user
        print(user)
        if not user.is_superuser and user not in board.members.all():
            raise PermissionDenied("You are not a member of this board.")

        serializer.save(creator=user)
    

class TaskListAssignToMeView(generics.ListAPIView):
    """List tasks assigned to the current user."""
    permission_classes = [IsAuthenticatedAndTAssignToMeOrSuperUser]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee=user)


class TaskListReviewingMeView(generics.ListAPIView):
    """List tasks where the current user is the reviewer."""
    permission_classes = [IsAuthenticatedAndRevieingOrSuperUser]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(reviewer=user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a task."""
    permission_classes = [IsAuthenticatedAndTaskRelatedOrSuperUser]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer



class TaskCommentListView(generics.ListCreateAPIView):
    """List or create comments for a specific task."""
    permission_classes = [IsAuthenticatedAndCommentRelatedOrSuperUser]
    queryset = Comment.objects.all()
    serializer_class = TaskCommentSerializer

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Comment.objects.filter(task_id=task_id).order_by('-created_at')
    
    def get_task(self):
        return get_object_or_404(Task, id=self.kwargs['task_id'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['task'] = self.get_task()
        return context

    def perform_create(self, serializer):
        serializer.save()


class TaskCommentDestroyView(generics.DestroyAPIView):
    """Delete a specific task comment."""
    permission_classes = [IsAuthenticatedAndSelf]
    queryset = Comment.objects.all()
    serializer_class = TaskCommentSerializer


