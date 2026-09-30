from django.contrib import admin

from .models import Submission, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "due_date", "created_at")
    filter_horizontal = ("students",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("task", "student", "status", "submitted_at")
    list_filter = ("status",)
