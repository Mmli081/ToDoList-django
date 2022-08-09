from django.contrib import admin
from .models import Day, Task
# Register your models here.

@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('date', 'user')
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("user", 'day')