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
        d1 = Day.objects.create(date=date(2022, 8, 1), user=sam)
        d2 = Day.objects.create(date=date(2022, 8, 2), user=sam)
        d3 = Day.objects.create(date=date(2022, 8, 2), user=hooman)
        d4 = Day.objects.create(date=date(2022, 8, 3), user=hooman)
        Task.objects.create(title="task1", day=d1, user=sam)
        Task.objects.create(title="task2", day=d2, user=sam)
        Task.objects.create(title="task3", day=d3, user=hooman)
        Task.objects.create(title="task4", day=d4, user=hooman)
        Task.objects.create(title="task5", type='everyday', user=hooman)
        Task.objects.create(title="task6", type='wednesday', user=hooman)

    def test_task_creation(self):
        task = Task.objects.get(title="task2")
        self.assertEqual(task.title, "task2")
        self.assertEqual(task.user.username, "sam")
        self.assertEqual(task.day.date, date(2022, 8, 2))
        self.assertEqual(task.description, None)
        self.assertEqual(task.has_done, False)
        self.assertEqual(task.type, "day")

    def test_day_creation(self):
        u = User.objects.get(username="sam")
        d = Day.get_or_create(date=date(2022, 8, 1), user=u)
        self.assertEqual(d, Day.objects.get(date=date(2022, 8, 1), user=u), "exist day not returned")
        self.assertEqual(Day.objects.count(), 4)
        d = Day.get_or_create(date=date(2022, 8, 4), user=u)
        self.assertEqual(d, Day.objects.get(date=date(2022, 8, 4), user=u), "new day not returned")
        self.assertEqual(Day.objects.count(), 5)

    def test_user_day_tasks(self):
        u = User.objects.get(username="hooman")
        day = Day.get_or_create(date=date(2022, 8, 3), user=u)
        tasks = day.get_user_tasks()
        self.assertEqual(tasks.count(), 3)
        day = Day.get_or_create(date=date(2022, 8, 2), user=u)
        tasks = day.get_user_tasks()
        self.assertEqual(tasks.count(), 2)
        day = Day.get_or_create(date=date(2022, 8, 1), user=u)
        tasks = day.get_user_tasks()
        self.assertEqual(tasks.count(), 1)
        u = User.objects.get(username="sam")
        day = Day.get_or_create(date=date(2022, 8, 3), user=u)
        tasks = day.get_user_tasks()
        self.assertEqual(tasks.count(), 0)
        day = Day.get_or_create(date=date(2022, 8, 2), user=u)
        tasks = day.get_user_tasks()
        self.assertEqual(tasks.count(), 1)
        day = Day.get_or_create(date=date(2022, 8, 1), user=u)
        tasks = day.get_user_tasks()
        self.assertEqual(tasks.count(), 1)
