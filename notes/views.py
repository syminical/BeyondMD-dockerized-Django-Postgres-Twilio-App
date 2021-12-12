from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.urls import reverse

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

def addList(request):
    if request.POST['newListName']:
        # this should be sanitized :(
        new_list_name = request.POST['newListName']
        if  len(new_list_name) <= TaskList._meta.get_field('name').max_length:
            l = TaskList(name=new_list_name)
            l.save()
            return HttpResponseRedirect(reverse('notes:index'))
        else:
            return render(request, 'notes/index.html', {
                'error_message': "That name is too long! (max 34 characters)"
            })
    else:
        return render(request, 'notes/index.html', {
            'error_message': "Please enter a name for the new list!"
        })