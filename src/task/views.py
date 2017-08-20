from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View


class TaskListView(View):
    template_name = 'task/tasks.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
