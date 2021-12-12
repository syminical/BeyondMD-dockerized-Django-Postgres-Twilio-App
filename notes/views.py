from django.shortcuts import render
from django.views import generic

from .models import Task, TaskList

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'notes/index.html'
    context_object_name = 'task_lists'

    def get_queryset(self):
        """
        Return all lists available.
        """
        return TaskList.objects.all()

class TaskListView(generic.DetailView):
    model = TaskList
    template_name = 'notes/list.html'