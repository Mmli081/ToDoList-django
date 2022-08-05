from django.test import TestCase
from datetime import date
from .models import Task, Day
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your tests here.

class TaskTestCase(TestCase):

    def setUp(self):
        sam = User.objects.create_user('sam', "sam", "sam")
        hooman = User.objects.create_user("hooman", "hooman", "hooman")
        d1 = Day.objects.create(date=date(2022, 8, 1))
        d2 = Day.objects.create(date=date(2022, 8, 2))
        d3 = Day.objects.create(date=date(2022, 8, 3))
        Task.objects.create(title="task1", user=sam, day=d1)
        Task.objects.create(title="task2", user=sam, day=d2)
        Task.objects.create(title="task3", user=hooman, day=d2)
        Task.objects.create(title="task4", user=hooman, day=d3)
        Task.objects.create(title="task5", user=hooman, type="everyday")
        Task.objects.create(title="task6", user=hooman, type="wednesday")

    def test_task_creation(self):
        task = Task.objects.get(title="task2")
        self.assertEqual(task.title, "task2")
        self.assertEqual(task.user.username, "sam")
        self.assertEqual(task.day.date, date(2022, 8, 2))
        self.assertEqual(task.description, None)
        self.assertEqual(task.has_done, False)
        self.assertEqual(task.type, "day")

    def test_get_day(self):
        d = Day.get_or_create(date=date(2022, 8, 1))
        self.assertEqual(d, Day.objects.get(date=date(2022, 8, 1)), "exist day not returned")
        d = Day.get_or_create(date=date(2022, 8, 4))
        self.assertEqual(d, Day.objects.get(date=date(2022, 8, 4)), "new day not returned")

    def test_user_day_tasks(self):
        u = User.objects.get(username="hooman")
        day = Day.objects.get(date=date(2022, 8, 3))
        tasks = day.get_user_tasks(u)
        self.assertEqual(tasks.count(), 3)
        day = Day.objects.get(date=date(2022, 8, 2))
        tasks = day.get_user_tasks(u)
        self.assertEqual(tasks.count(), 2)
        day = Day.objects.get(date=date(2022, 8, 1))
        tasks = day.get_user_tasks(u)
        self.assertEqual(tasks.count(), 1)
        u = User.objects.get(username="sam")
        day = Day.objects.get(date=date(2022, 8, 3))
        tasks = day.get_user_tasks(u)
        self.assertEqual(tasks.count(), 0)
        day = Day.objects.get(date=date(2022, 8, 2))
        tasks = day.get_user_tasks(u)
        self.assertEqual(tasks.count(), 1)
        day = Day.objects.get(date=date(2022, 8, 1))
        tasks = day.get_user_tasks(u)
        self.assertEqual(tasks.count(), 1)
