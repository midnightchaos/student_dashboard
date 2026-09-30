from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from tasks.forms import SubmissionForm, TaskForm
from tasks.models import Submission, Task

from accounts.models import User


def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role != role:
                messages.error(request, "You are not allowed to access that page.")
                return redirect("home")
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


teacher_required = role_required(User.TEACHER)
student_required = role_required(User.STUDENT)


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.is_teacher:
        return redirect("teacher_dashboard")
    return redirect("student_dashboard")


# ---------------- Teacher ----------------


@teacher_required
def teacher_dashboard(request):
    tasks = Task.objects.filter(teacher=request.user)
    context = {
        "tasks": tasks,
        "student_count": User.objects.filter(role=User.STUDENT).count(),
        "pending_count": Submission.objects.filter(
            task__teacher=request.user, status=Submission.PENDING
        ).count(),
        "submitted_count": Submission.objects.filter(
            task__teacher=request.user, status=Submission.SUBMITTED
        ).count(),
    }
    return render(request, "dashboard/teacher_dashboard.html", context)


@teacher_required
def teacher_students(request):
    students = User.objects.filter(role=User.STUDENT)
    return render(request, "dashboard/teacher_students.html", {"students": students})


@teacher_required
def teacher_tasks(request):
    tasks = Task.objects.filter(teacher=request.user)
    return render(request, "dashboard/teacher_tasks.html", {"tasks": tasks})


@teacher_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.teacher = request.user
            task.save()
            form.save_m2m()
            messages.success(request, "Task created and assigned.")
            return redirect("teacher_tasks")
    else:
        form = TaskForm()
    return render(request, "dashboard/task_form.html", {"form": form})


@teacher_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, teacher=request.user)
    submissions = task.submissions.select_related("student")
    submitted = {s.student_id for s in submissions if s.status == Submission.SUBMITTED}
    rows = [
        {"student": student, "submission": next(
            (s for s in submissions if s.student_id == student.pk), None
        )}
        for student in task.students.all()
    ]
    return render(
        request,
        "dashboard/teacher_task_detail.html",
        {"task": task, "rows": rows, "submitted_count": len(submitted)},
    )


# ---------------- Student ----------------


@student_required
def student_dashboard(request):
    tasks = request.user.assigned_tasks.all()
    submitted_ids = Submission.objects.filter(
        student=request.user, status=Submission.SUBMITTED
    ).values_list("task_id", flat=True)
    context = {
        "tasks": tasks,
        "pending_count": len([t for t in tasks if t.pk not in submitted_ids]),
        "submitted_count": len([t for t in tasks if t.pk in submitted_ids]),
    }
    return render(request, "dashboard/student_dashboard.html", context)


@student_required
def student_tasks(request):
    tasks = request.user.assigned_tasks.all()
    submitted_ids = set(
        Submission.objects.filter(
            student=request.user, status=Submission.SUBMITTED
        ).values_list("task_id", flat=True)
    )
    return render(
        request,
        "dashboard/student_tasks.html",
        {"tasks": tasks, "submitted_ids": submitted_ids},
    )


@student_required
def student_task_detail(request, pk):
    task = get_object_or_404(request.user.assigned_tasks, pk=pk)
    submission = Submission.objects.filter(task=task, student=request.user).first()
    return render(
        request,
        "dashboard/student_task_detail.html",
        {"task": task, "submission": submission},
    )


@student_required
def student_task_submit(request, pk):
    task = get_object_or_404(request.user.assigned_tasks, pk=pk)
    submission = Submission.objects.filter(task=task, student=request.user).first()

    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.task = task
            obj.student = request.user
            obj.status = Submission.SUBMITTED
            obj.save()
            messages.success(request, "Task submitted.")
            return redirect("student_task_detail", pk=pk)
    else:
        form = SubmissionForm(instance=submission)

    return render(
        request, "dashboard/student_task_submit.html", {"task": task, "form": form}
    )
