from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(max_length=500, verbose_name="Описание",
                                   blank=True)
    is_done = models.BooleanField(verbose_name="Выполнено", default=False)
    user_added = models.ForeignKey(User, verbose_name="Пользователь")
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name="Дата создания")

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return self.name
