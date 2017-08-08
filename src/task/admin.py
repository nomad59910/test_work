from django.contrib import admin
from .models import Task, CompletedTask
# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_done', )

    # def is_done_total(self, obj):
    #     completed_task = get_or_none(CompletedTask, task=obj)
    #     if completed_task:
    #         return "<h3>NONE</h3>"
    #     else:
    #         return "<h3>NONE</h3>"
    #
    # is_done_total.short_description = 'Выполнено'
    # is_done_total.allow_tags = True


admin.site.register(Task, TaskAdmin)
admin.site.register(CompletedTask)
