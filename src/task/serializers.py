from rest_framework import serializers
from .models import Task


class TaskSerializers(serializers.ModelSerializer):
    user_added = serializers.CharField(source='user_added.username')
    is_done = serializers.SerializerMethodField('is_done')

    def is_done(self, obj):
        return obj.is_done()

    class Meta:
        model = Task
        fields = ('name', 'description', 'user_added', 'date_created', 'id',
                  'is_done', )
