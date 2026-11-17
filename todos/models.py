from django.db import models

class Todo(models.Model):
    status_choices = [
        ("OPEN", "open"),
        ("IN_PROGRESS", "in progress"),
        ("COMPLETED", "completed"),
    ]

    title = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=status_choices,
        default="OPEN"
    )
    created_at = models.DateField(auto_now_add=True)

    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
