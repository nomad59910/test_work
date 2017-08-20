from django.contrib import admin
from .models import Task
# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_done', )


admin.site.register(Task, TaskAdmin)
