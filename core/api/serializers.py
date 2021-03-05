from rest_framework import serializers
from core.models import TodoList


class TodoListSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(max_length=15)
    # date_created = serializers.CharField(max_length=15)
    class Meta:
        model=TodoList
        fields=('user', 'date_created')