from accounts.models import User
from tasks.models import Task, Submission

def u(name, role):
    obj, _ = User.objects.get_or_create(username=name, defaults={"role": role, "email": name + "@college.edu"})
    obj.role = role
    obj.set_password("pass1234")
    obj.save()
    return obj

teacher = u("john", User.TEACHER)
students = [u(n, User.STUDENT) for n in ["rahul", "ronek", "akhil", "vishnu"]]

task, created = Task.objects.get_or_create(
    title="Django Assignment",
    defaults={
        "description": "Create a CRUD application with models, forms and templates.",
        "teacher": teacher,
        "due_date": "2026-09-30",
    },
)
task.students.set(students)

sub, _ = Submission.objects.get_or_create(task=task, student=students[0])
sub.answer = "Here is my CRUD app."
sub.status = Submission.SUBMITTED
sub.save()

print("seeded", User.objects.count(), "users,", Task.objects.count(), "tasks")
