from django.conf import settings
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks_created"
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="assigned_tasks", blank=True
    )
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Submission(models.Model):
    PENDING = "Pending"
    SUBMITTED = "Submitted"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (SUBMITTED, "Submitted"),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions"
    )
    answer = models.TextField(blank=True)
    file = models.FileField(upload_to="submissions/", blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

    class Meta:
        unique_together = ("task", "student")

    def __str__(self):
        return f"{self.student} - {self.task}"
