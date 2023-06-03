from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.
def index(request) :
    if request.user.is_authenticated:
        tasks= Task.objects.filter(user=request.user).order_by("-time")
        return render(request, "tasks/index.html", {
            "taskForm": AddNewTask(),
            "allTasks": tasks
        })
    return render(request, "tasks/index.html")

def login_view(request) :
    if request.method == "POST" :
        username= request.POST["username"]
        password= request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None :
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else :
            return render(request, "tasks/login.html", {
                "message": "Invalid username OR/AND password"
            })

    return render(request, "tasks/login.html")

def logout_view(request) :
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request) :
    if request.method == "POST" :
        username= request.POST["username"]
        email= request.POST["email"]
        password= request.POST["password"]
        confirmation= request.POST["confirmation"]

        if password != confirmation :
            return render(request, "tasks/register.html", {
                "message": "passwords must match!"
            })
        
        try :
            user= User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError :
            return render(request, "tasks/register.html", {
                "message": "User already taken"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "tasks/register.html")

@login_required
def addTask(request):
    if request.method == "POST":
        form= AddNewTask(request.POST)
        if form.is_valid():
            form.fields["user"]= request.POST["user"]
            form.save()
            return HttpResponseRedirect(reverse("index"))

@login_required        
def taskDone(request, ID):
    task= Task.objects.get(pk=ID)
    task.done= True
    task.save(update_fields=['done'])
    return HttpResponseRedirect(reverse("index"))    