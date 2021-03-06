import os

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse

from .models import Auth, Task, TaskList

from twilio.rest import Client
# Create your views here.

authyClient = Client(os.environ['AUTHY_SID'], os.environ['AUTHY_SECRET'])

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
                'error_message': "That name is too long! (max 34 characters)",
                'task_lists': TaskList.objects.all()
            })
    else:
        return render(request, 'notes/index.html', {
            'error_message': "Please enter a name for the new list!",
            'task_lists': TaskList.objects.all()
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
class RenameTaskView(generic.DetailView):
    model = Task
    template_name = 'notes/renameTask.html'

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
            l = get_object_or_404(TaskList, pk=tasklist_id) # make sure list exists
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

def updateTaskText(request, task_id):
    print(request.POST)
    if request.POST['newTaskText']:
        # this should be sanitized :(
        new_task_text = request.POST['newTaskText']
        if  len(new_task_text) <= Task._meta.get_field('text').max_length:
            # user access should be checked
            t = get_object_or_404(Task, pk=task_id)
            t.text = new_task_text
            t.save()
            return HttpResponseRedirect(reverse('notes:list', args=[t.task_list.id]))
        else:
            return render(request, 'notes/renameTask.html', {
                'error_message': "That name is too long! (max 34 characters)",
                'task': get_object_or_404(Task, pk=task_id)
            })
    else:
        return render(request, 'notes/renameTask.html', {
            'error_message': "Please enter some text for the task!",
            'task': get_object_or_404(Task, pk=task_id)
        })

# authy
def addAuth(request):
    if request.POST['phoneNumber']:
        # this should be sanitized :(
        phone_number = request.POST['phoneNumber']
        if  len(phone_number) == 10:
            
            if Auth.objects.all():
                a = Auth.objects.get(pk=1)
                a.number = f'+1{phone_number}'
            else:
                a = Auth(number=f'+1{phone_number}')
            a.save()
            v = authyClient.verify.services(os.environ['AUTHY_SERVICE']).verifications.create(to=a.number, channel='sms')
            return render(request, 'notes/index.html', {
                'auth_message': "Authy request sent! Enter your code to verify.",
                'task_lists': TaskList.objects.all()
            })
        else:
            return render(request, 'notes/index.html', {
                'auth_message': "That is too long! Start with the area code (max 10 characters)",
                'task_lists': TaskList.objects.all()
            })
    else:
        return render(request, 'notes/index.html', {
            'auth_message': "Please enter a phone number, starting with the area code!",
            'task_lists': TaskList.objects.all()
        })

def verifyAuth(request):
    if request.POST['code']:
        # this should be sanitized :(
        code = request.POST['code']
        if  len(code) == 6:
            a = Auth.objects.get(pk=1)
            if a:
                v = authyClient.verify.services(os.environ['AUTHY_SERVICE']).verification_checks.create(to=a.number, code=code)
                return render(request, 'notes/index.html', {
                    'auth_message': f'Authy verify status: {v.status}',
                    'task_lists': TaskList.objects.all()
                })
            else:
                return render(request, 'notes/index.html', {
                    'auth_message': "Enter a phone number above first to verify.",
                    'task_lists': TaskList.objects.all()
                })
        else:
            return render(request, 'notes/index.html', {
                'auth_message': "The authy code should be 6 digits.",
                'task_lists': TaskList.objects.all()
            })