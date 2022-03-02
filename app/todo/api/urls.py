from django.urls import path
from .views import TaskListView, TaskDetailView, TaskExecView

urlpatterns = [
    path("", TaskListView.as_view()),
    path("<task_id>/", TaskDetailView.as_view()),
    path("<task_id>/execute/", TaskExecView.as_view()),
]
