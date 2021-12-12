from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('list/<int:pk>', views.TaskListView.as_view(), name='list')
]