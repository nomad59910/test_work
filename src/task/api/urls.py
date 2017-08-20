from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from task.api.api import (
    TasksList,
    TaskUpdateAPIView,
    TaskCreateAPIView,
    TaskDeleteAPIView,
    DoneTaskAPIView,
    UndoneTaskAPIView
)

app_name = 'task_api'

urlpatterns = [
    url(r'^list/$', TasksList.as_view(), name="list"),
    url(r'^add/$', TaskCreateAPIView.as_view(), name="add"),
    url(r'^edit/(?P<id>[0-9]+)/$', TaskUpdateAPIView.as_view(), name="edit"),
    url(r'^delete/(?P<id>[0-9]+)/$', TaskDeleteAPIView.as_view(), name="delete"),
    url(r'^done/(?P<id>[0-9]+)/$', DoneTaskAPIView.as_view(), name="done"),
    url(r'^undone/(?P<id>[0-9]+)/$', UndoneTaskAPIView.as_view(), name="undone"),
]
