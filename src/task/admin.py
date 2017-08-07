from django.contrib import admin
from .models import Task, CompletedTask
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('name',), }
    readonly_fields = ('is_done', )
    list_display = ('name', 'is_done', )
    fields = ('name', 'description', )


admin.site.register(Task, TaskAdmin)
admin.site.register(CompletedTask)
