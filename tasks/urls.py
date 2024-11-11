#tasks urls 
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('task/create/', views.create_task, name ='create_task' ),
    path('task/detail/<int:task_id>' , views.task_detail, name='task_detail'),
    path('task/<int:task_id>/complete' , views.task_complete, name='task_complete'),
    path('task/<int:task_id>/delete', views.task_delete, name='task_delete'),
    path('tasks/completed', views.tasks_completed, name='task_completed')    
    ]