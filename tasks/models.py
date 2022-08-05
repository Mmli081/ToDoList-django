from datetime import datetime

from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
days_choices = (('day', 'Day'),
                ('everyday', 'EveryDay'),
                ('monday', 'Mondays'),
                ('tuesday', 'Tuesdays'),
                ('wednesday', 'Wednesdays'),
                ('thursday', 'Thursdays'),
                ('friday', 'Fridays'),
                ('saturday', 'Saturdays'),
                ('sunday', 'Sundays'),
                )


class Day(models.Model):
    date = models.DateField()

    @staticmethod
    def get_or_create(date):
        try:
            day = Day.objects.get(date=date)
        except Day.DoesNotExist:
            day = Day.objects.create(date=date)
        return day

    def get_user_tasks(self, user):
        self.tasks.set(Task.objects.filter(day=self, user=user))
        day_name = self.date.strftime('%A').lower()
        multi_tasks = Task.objects.filter(~Q(type='day') & Q(user=user))
        for task in multi_tasks:
            if task.type in [day_name, 'everyday']:
                Task.objects.create(
                    title=task.title, user=user, day=self, description=task.description, type='day')
        return self.tasks

    def __str__(self):
        return self.date.strftime('%A')


class Task(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="days")
    day = models.ForeignKey(Day, on_delete=models.CASCADE, null=True, related_name="tasks")
    description = models.TextField(null=True, blank=True)
    has_done = models.BooleanField(default=False)
    type = models.CharField(max_length=10, default="day", choices=days_choices)

    def __str__(self):
        return self.title
