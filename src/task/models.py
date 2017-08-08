from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


class Task(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(max_length=500, verbose_name="Описание",
                                   blank=True)
    user_added = models.ForeignKey(User, verbose_name="Пользователь")
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name="Дата создания")

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.name

    def complet(self, user):
        CompletedTask.objects.create(user=user, task=self)

    def is_done(self):
        if get_or_none(CompletedTask, task=self):
            return True
        else:
            return False

    is_done.boolean = True
    is_done.short_description = "Выполнено"

class CompletedTask(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь")
    task = models.OneToOneField(Task, verbose_name="Задание")

    class Meta:
        verbose_name = 'Выполненное задание'
        verbose_name_plural = 'Выполненные задания'

    def __str__(self):
        return self.task.__str__()
