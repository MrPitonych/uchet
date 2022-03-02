from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TaskSerializer
from ..models import Task
from app.tasks import send_result


class TaskListView(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        tasks = Task.objects.all()
        task_serializer = TaskSerializer(tasks, many=True)
        return Response(task_serializer.data, status=200)

    @staticmethod
    def post(request):
        task_serializer = TaskSerializer(data=request.data)
        if task_serializer.is_valid():
            task_serializer.save()
            return Response("task created", status=201)
        return Response("failed to create task", status=400)


class TaskDetailView(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(requset, task_id):
        try:
            task = Task.objects.get(pk=task_id)
            task_serializer = TaskSerializer(task, many=False)
            return Response(task_serializer.data, status=200)
        except Task.DoesNotExist:
            return Response("task not found", status=400)

    @staticmethod
    def patch(request, task_id):
        try:
            task = Task.objects.get(pk=task_id)
            task_serializer = TaskSerializer(
                task, data=request.data, many=False, partial=True
            )
            if task_serializer.is_valid():
                task_serializer.save()
                return Response(task_serializer.data, 200)
            return Response(task_serializer.errors, 400)
        except Task.DoesNotExist:
            return Response("task not found", status=400)

    @staticmethod
    def delete(request, task_id):
        try:
            task = Task.objects.get(pk=task_id)
            task.delete()
            return Response("task deleted", status=200)
        except Task.DoesNotExist:
            return Response("task not found", status=400)


class TaskExecView(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, task_id):

        try:
            task = Task.objects.get(pk=task_id)
            if task.is_executed is True:
                return Response("task already completed", status=200)
            task.is_executed = True
            task.save()
            task_serializer = TaskSerializer(task)
            send_result.delay(request.user.email, task.title)
            return Response(task_serializer.data, status=200)
        except Task.DoesNotExist:
            return Response("task not found", status=400)
