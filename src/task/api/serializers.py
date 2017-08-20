from rest_framework import serializers
from task.models import Task


class TaskSerializers(serializers.ModelSerializer):
    user_added = serializers.CharField(source='user_added.username')

    class Meta:
        model = Task
        fields = ('name', 'description', 'user_added', 'date_created', 'id',
                  'is_done', )


class TaskUpdateSerializers(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('name', 'description', )


class TaskCreateSerializers(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('name', 'description', 'date_created', 'id', 'is_done', )

class TaskUpdateIsDoneSerializers(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('is_done', )
