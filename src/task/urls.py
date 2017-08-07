from django.conf.urls import url
from .views import TaskListView
from django.contrib.auth.decorators import login_required
from .api import TasksList

app_name = 'task'

urlpatterns = [
    url(r'^tasks/$', login_required(TaskListView.as_view()), name="tasks"),
    url(r'^api/tasks-list$', TasksList.as_view(), name="tasks-list"),
]
