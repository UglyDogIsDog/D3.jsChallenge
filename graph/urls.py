from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'graph'

urlpatterns = [
    path('index/', views.index, name='index'),
    url(r'^api/task_1', views.task_1, name='task_1'),
    url(r'^api/task_2', views.task_2, name='task_2'),
    url(r'^api/task_3', views.task_3, name='task_3'),
]