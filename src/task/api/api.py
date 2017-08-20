from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    CreateAPIView,
    DestroyAPIView
    )

from .serializers import (
    TaskSerializers,
    TaskUpdateSerializers,
    TaskCreateSerializers,
    TaskUpdateIsDoneSerializers,
)

from task.models import Task
from .permissions import IsAddedAuthorizedUser


class TasksList(ListAPIView):
    serializer_class = TaskSerializers
    # pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self, *args, **kwargs):
        queryset_list = Task.objects.filter(user_added=self.request.user)
        is_done = self.request.GET.get("done")
        if is_done:
            queryset_list = queryset_list.filter(is_done=is_done)

        prev_id = self.request.GET.get("prev_id")
        if prev_id:
            queryset_list = queryset_list.filter(id__lt=prev_id)

        limit = self.request.GET.get("limit")
        if limit:
            queryset_list = queryset_list[:int(limit)]

        return queryset_list


class TaskUpdateAPIView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializers
    permission_classes = [IsAuthenticated, IsAddedAuthorizedUser, ]
    lookup_field = "id"


class TaskDeleteAPIView(DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers
    lookup_field = "id"
    permission_classes = [IsAuthenticated, IsAddedAuthorizedUser, ]


class TaskCreateAPIView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializers
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializers):
        serializers.save(user_added=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        task_id = serializer.data['id']
        task = Task.objects.get(id=task_id)
        serializer = TaskSerializers(task)

        return Response(dict(serializer.data), status=status.HTTP_201_CREATED,
                        headers=headers)


class DoneTaskAPIView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskUpdateIsDoneSerializers
    permission_classes = [IsAuthenticated, IsAddedAuthorizedUser, ]
    lookup_field = "id"

    def perform_update(self, serializer):
        serializer.save(is_done=True)


class UndoneTaskAPIView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskUpdateIsDoneSerializers
    permission_classes = [IsAuthenticated, IsAddedAuthorizedUser, ]
    lookup_field = "id"

    def perform_update(self, serializer):
        serializer.save(is_done=False)
