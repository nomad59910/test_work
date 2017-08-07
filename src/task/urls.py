from django.conf.urls import url
from .views import TaskListView
from django.contrib.auth.decorators import login_required

app_name = 'task'

urlpatterns = [
    url(r'^tasks/$', login_required(TaskListView.as_view()), name="tasks"),
]
