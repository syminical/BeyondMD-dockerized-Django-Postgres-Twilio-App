from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse

from .models import Task, TaskList

# Create your views here.

# Task Lists
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

class RenameListView(generic.DetailView):
    model = TaskList
    template_name = 'notes/renameList.html'

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

def deleteList(request, list_id):
    # user access should be checked
    l = get_object_or_404(TaskList, pk=list_id)
    l.delete()
    return HttpResponseRedirect(reverse('notes:index'))

def updateListName(request, list_id):
    if request.POST['newListName']:
        # this should be sanitized :(
        new_list_name = request.POST['newListName']
        if  len(new_list_name) <= TaskList._meta.get_field('name').max_length:
            # user access should be checked
            l = get_object_or_404(TaskList, pk=list_id)
            l.name = new_list_name
            l.save()
            return HttpResponseRedirect(reverse('notes:index'))
        else:
            return render(request, 'notes/renameList.html', {
                'error_message': "That name is too long! (max 34 characters)",
                'tasklist': get_object_or_404(TaskList, pk=list_id)
            })
    else:
        return render(request, 'notes/renameList.html', {
            'error_message': "Please enter a new list name!",
            'tasklist': get_object_or_404(TaskList, pk=list_id)
        })

# Tasks
def toggleTask(request, tasklist_id, task_id):
    # user access should be checked
    t = get_object_or_404(Task, pk=task_id)
    t.completed = not t.completed
    t.save()
    return HttpResponseRedirect(reverse('notes:list', args=[tasklist_id]))

def addTask(request, tasklist_id):
    if request.POST['newTaskText']:
        # this should be sanitized :(
        new_task_text = request.POST['newTaskText']
        if  len(new_task_text) <= Task._meta.get_field('text').max_length:
            # user access should be checked
            get_object_or_404(TaskList, pk=tasklist_id) # make sure list exists
            t = Task(task_list=l, text=new_task_text)
            t.save()
            return HttpResponseRedirect(reverse('notes:list', args=[tasklist_id]))
        else:
            return render(request, 'notes/list.html', {
                'error_message': "That is too long! (max 120 characters)",
                'tasklist': get_object_or_404(TaskList, pk=tasklist_id)
            })
    else:
        return render(request, 'notes/list.html', {
            'error_message': "Please enter some text for the new task!",
            'tasklist': get_object_or_404(TaskList, pk=tasklist_id)
        })

def deleteTask(request, tasklist_id, task_id):
    # user access should be checked
    t = get_object_or_404(Task, pk=task_id)
    t.delete()
    return HttpResponseRedirect(reverse('notes:list', args=[tasklist_id]))