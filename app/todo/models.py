from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    execution_date = models.DateTimeField(auto_now_add=True)
    is_executed = models.BooleanField(default=False)

    class Meta:
        ordering = ["execution_date"]

    def __str__(self):
        return f"{self.pk} {self.title}"
