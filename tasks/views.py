from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Task, Day
from .serializers import *
from .time_utils import create_date

# Create your views here.


class TaskListAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskCreateAPI(CreateAPIView):
    permission_classes = (IsAuthenticated, )

    serializer_class = TaskCreateSerializer

    def perform_create(self, serializer):
        str_date = self.request.data.get('day')
        day = Day.get_or_create(create_date(str_date), self.request.user) if str_date else None
        serializer.save(user=self.request.user, day=day)


class DayTaskAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, day):
        day = Day.get_or_create(create_date(day), self.request.user)
        tasks = day.get_user_tasks()
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)