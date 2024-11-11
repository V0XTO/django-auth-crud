from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
# => Libreria para guardar sesión
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
# Create your views here.
from .forms import CreateTaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(req):
    return render(req, 'home.html')

def signup(req):
    
    if req.method == 'GET':
        return render(req,'signup.html', {
            'form': UserCreationForm
        })
    else:
          if req.POST['password1'] == req.POST['password2']:
            try:
                user = User.objects.create_user(username=req.POST['username'], password=req.POST['password1'])
                user.save()
                # => Guardar Sesión en el navegador (crea una cokie)
                login(req,user)
                return redirect('tasks')
            except IntegrityError:
                return render(req, 'signup.html',{
                    'form': UserCreationForm,
                    'error': 'User already exist'
                })
          return render(req, 'signup.html', {
              'form': UserCreationForm,
              'error': 'password do not match'
          })
@login_required
def tasks(req):
    try:
        print(req)
        tasks = Task.objects.filter(user= req.user, datecompleted__isnull = True)
    
        return render(req,'tasks.html', {
            'tasks': tasks
        })
    except:
        return render(req,'tasks.html')



@login_required
def signout(req):
    logout(req)
    return redirect('home')

def signin(req):
    if req.method == 'GET':
        return render(req, 'signin.html',{
            'form': AuthenticationForm
        })
    else:
        user= authenticate(req, username = req.POST['username'], password = req.POST['password'])
        #Si el usuario no es valido 
        if user is None: 
            return render(req, 'signin.html',{
                'form':AuthenticationForm,
                'error': 'user o password incorrect'
            })
        
        #Si el usuario es valido
        else:
            login(req, user )
            return redirect('tasks')
            
@login_required
def create_task(req):
    if req.method == 'GET':
        return  render(req, 'create_task.html', {
            'form': CreateTaskForm
        })
    else:
        try:
            form = CreateTaskForm(req.POST)
            new_task = form.save(commit=False)
            new_task.user= req.user
            new_task.save()
            return redirect('tasks')
        except:
             return  render(req, 'create_task.html', {
                'form': CreateTaskForm,
                'error': 'error'
             })
        
@login_required
def task_detail(req, task_id):
    if req.method == 'GET':
        
        try:
            # OBTENER SOLAMENTE MIS TAREAS Y NO LAS DE OTROS USUARIOS
            task = get_object_or_404(Task.objects.filter(user = req.user) , pk = task_id)
            form = CreateTaskForm(instance=task)
            return render(req ,'task_detail.html',{
                'task': task,
                'form': form
            })
        except:

            return render(req ,'task_detail.html',{
                'not_found': 'Task Not Found'
            })
    else:
        try:
            
            task = get_object_or_404(Task,pk = task_id)
            form = CreateTaskForm(req.POST, instance=task)
            form.save() 

            return redirect('tasks')
        except ValueError :
            return render(req, 'task_detail.html',{
                'task': task,
                'form': form,
                'error':  'error updating Task'
            })


@login_required
def task_complete(req, task_id):
    task = get_object_or_404(Task.objects.filter(user= req.user), pk=task_id)
    if req.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
@login_required
def task_delete(req, task_id):
    task = get_object_or_404(Task.objects.filter(user= req.user), pk=task_id)
    task.delete()
    return redirect('tasks')

@login_required
def tasks_completed(req):

    tasks = Task.objects.filter(user= req.user, datecompleted__isnull = False)

    return render(req, 'task_completed.html', {'tasks': tasks})