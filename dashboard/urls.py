from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # Teacher
    path("teacher/dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("teacher/students/", views.teacher_students, name="teacher_students"),
    path("teacher/tasks/", views.teacher_tasks, name="teacher_tasks"),
    path("teacher/tasks/create/", views.task_create, name="task_create"),
    path("teacher/tasks/<int:pk>/", views.task_detail, name="teacher_task_detail"),
    # Student
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("student/tasks/", views.student_tasks, name="student_tasks"),
    path("student/tasks/<int:pk>/", views.student_task_detail, name="student_task_detail"),
    path(
        "student/tasks/<int:pk>/submit/",
        views.student_task_submit,
        name="student_task_submit",
    ),
]
