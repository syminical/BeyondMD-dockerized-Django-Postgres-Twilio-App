from django.urls import path

from . import views

app_name = 'notes'
urlpatterns = [
    # task lists
    path('', views.IndexView.as_view(), name='index'),
    path('list/<int:pk>', views.TaskListView.as_view(), name='list'),
    path('addList', views.addList, name='addList'),
    path('deleteList/<int:list_id>', views.deleteList, name='deleteList'),
    path('renameList/<int:pk>', views.RenameListView.as_view(), name='renameList'),
    path('updateListName/<int:list_id>', views.updateListName, name='updateListName'),
    # tasks
    path('toggleTask/<int:tasklist_id>/<int:task_id>', views.toggleTask, name='toggleTask'),
    path('addTask/<int:tasklist_id>', views.addTask, name='addTask'),
    path('deleteTask/<int:tasklist_id>/<int:task_id>', views.deleteTask, name='deleteTask'),
    path('renameTask/<int:pk>', views.RenameTaskView.as_view(), name='renameTask'),
    path('updateTaskName/<int:task_id>', views.updateTaskText, name='updateTaskText'),
    path('addAuth', views.addAuth, name='addAuth'),
    path('verifyAuth', views.verifyAuth, name='verifyAuth')
]