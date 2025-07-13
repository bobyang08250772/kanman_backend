from django.urls import path
from .views import BoardListView, BoardDetailView, TaskListView, TaskCommentListView, TaskCommentDestroyView, TaskDetailView, TaskListAssignToMeView, TaskListReviewingMeView

urlpatterns = [
    path('api/boards/', BoardListView.as_view(), name='board-list'),
    path('api/boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
    path('api/tasks/', TaskListView.as_view(), name='task-list'),
    path('api/tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('api/tasks/assigned-to-me/', TaskListAssignToMeView.as_view(), name='task-detail-assigned-to-me'),
    path('api/tasks/reviewing/', TaskListReviewingMeView.as_view(), name='task-detail-assigned-to-me'),
    path('api/tasks/<int:task_id>/comments/', TaskCommentListView.as_view(), name='task-comment-list'),
    path('api/tasks/<int:task_id>/comments/<int:pk>/', TaskCommentDestroyView.as_view(), name='task-comment-delete')
]
