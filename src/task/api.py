from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from .serializers import TaskSerializers
from .models import Task


class TasksList(ListAPIView):
    serializer_class = TaskSerializers
    pagination_class = LimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Task.objects.all()
        return queryset_list
