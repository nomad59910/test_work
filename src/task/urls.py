from django.conf.urls import url
from .views import TaskListView

app_name = 'task'

urlpatterns = [
    url(r'^tasks/$', TaskListView.as_view(), name="tasks"),
]
