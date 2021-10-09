from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q

from .models import *
from .forms import *
# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains = q) |
        Q(description__icontains=q))
    
    topics = Topic.objects.all()
    context={'rooms':rooms,'topics':topics}
    return render(request,'core/home.html',context)


def room(request,pk):
    room= Room.objects.get(id=pk)
    context={'rooms':room}
    return render(request,'core/room.html',context)


def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'core/roomForm.html',context)


def updateRoom(request,pk):
    room= Room.objects.get(id=pk)
    form = RoomForm(instance=room)
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
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context={'room':room}
    return render(request,'core/delete.html',context)