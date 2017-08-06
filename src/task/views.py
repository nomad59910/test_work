from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View

# Create your views here.

class TaskListView(View):
    template_name = 'task/tasks.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs
        return render(request, self.template_name)

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         # <process form cleaned data>
    #         return HttpResponseRedirect('/success/')
    #
    #     return render(request, self.template_name, {'form': form})
