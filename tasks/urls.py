from django.urls import path
from . import views

urlpatterns = [
    path("", views.TaskListAPI.as_view(), name="tasks"),
    path("create/", views.TaskCreateAPI.as_view(), name="task_create"),
    path("<slug:day>/", views.DayTaskAPI.as_view(), name="day_tasks"),
]