from django.urls import path

from . import views

app_name = 'notes'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('list/<int:pk>', views.TaskListView.as_view(), name='list'),
    path('addList', views.addList, name='addList'),
    path('deleteList/<int:list_id>', views.deleteList, name='deleteList')
]