from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    TEACHER = "Teacher"
    STUDENT = "Student"
    ROLE_CHOICES = [
        (TEACHER, "Teacher"),
        (STUDENT, "Student"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT)

    @property
    def is_teacher(self):
        return self.role == self.TEACHER

    @property
    def is_student(self):
        return self.role == self.STUDENT
