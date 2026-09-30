from django import forms

from .models import Submission, Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "students"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "students": forms.CheckboxSelectMultiple,
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["answer", "file"]
        widgets = {"answer": forms.Textarea(attrs={"rows": 5})}
