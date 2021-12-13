from django.db import models

# Create your models here.

# One TaskList can have 0 or more Tasks.
class TaskList(models.Model):
    name = models.CharField(max_length=34)

    def __str__(self):
        return self.name

# One Task belongs to one TaskList.
class Task(models.Model):
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    text = models.CharField(max_length=120)

    def __str__(self):
        return self.text