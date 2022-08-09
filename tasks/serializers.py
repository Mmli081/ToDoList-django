from rest_framework import serializers

from .models import Task, Day
from .time_utils import create_date


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'type')

    def validate(self, data):
        if data.get('type') == 'day':
            if self.initial_data.get('day') is None:
                raise serializers.ValidationError('Day is required')
            if create_date(self.initial_data.get('day')) == None:
                raise serializers.ValidationError('Day is invalid')
        else:
            if self.initial_data.get('day') is not None:
                raise serializers.ValidationError('Day is expected to be null')
        return data

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