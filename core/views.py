from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import *
from .forms import *
# Create your views here.


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error occurred during registration. Try Again!!")

    context={'form':form}
    return render(request,'core/login_register.html',context)


def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"User Not Found")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Username or Password does not exsist")

    context={'page':page}
    return render(request,'core/login_register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains = q) |
        Q(description__icontains=q)
        )
    
    topics = Topic.objects.all()
    roomCount = rooms.count()
    context={'rooms':rooms,'topics':topics,'roomCount':roomCount}
    return render(request,'core/home.html',context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all().order_by('-created') 
    context={'rooms':room,'messages':messages}
    return render(request,'core/room.html',context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'core/roomForm.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room= Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You do not have host permission")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'core/roomForm.html',context)


def deleteRoom(request,pk):
    room= Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You do not have host permission")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context={'room':room}
    return render(request,'core/delete.html',context)