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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='days')

    @staticmethod
    def get_or_create(date, user):
        try:
            day = Day.objects.get(date=date, user=user)
        except Day.DoesNotExist:
            day = Day.objects.create(date=date, user=user)
        return day

    def get_user_tasks(self):
        day_name = self.date.strftime('%A').lower()
        all_tasks = Task.objects.filter(user=self.user)
        for task in all_tasks:
            if task.type in ['everyday', day_name]:
                Task.objects.create(title=task.title, user=self.user, day=self, description=task.description,)
        return self.tasks

    def __str__(self):
        return f"{self.date} from {self.user}"


class Task(models.Model):
    title = models.CharField(max_length=200)
    day = models.ForeignKey(Day, on_delete=models.CASCADE, null=True, related_name="tasks")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField(null=True, blank=True)
    has_done = models.BooleanField(default=False)
    type = models.CharField(max_length=10, default="day", choices=days_choices)

    def __str__(self):
        return self.title
