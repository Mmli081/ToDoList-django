from rest_framework import serializers

from .models import Task, Day


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'type')

    def create(self, validated_data):
        return Task.objects.create(**validated_data)
    

class TaskListSerializer(serializers.ModelSerializer):
    day = serializers.ReadOnlyField(source='day.date')
    class Meta:
        model = Task
        exclude = ('user',)


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ('date',)