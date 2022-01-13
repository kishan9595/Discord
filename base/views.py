from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User

def loginPage(request):
    context = {}
    if request.POST.get('username'):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            pass    

    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(content__icontains=q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics':topics, 'room_count':room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id = pk)
    context = {'room': room}        

    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)    


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
           form.save()
        return redirect('home')
            
    context = {'form':form}
    return render(request, 'base/room_form.html', context) 

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')

    context = {'room':room}
    return render(request, 'base/delete.html', context) 






















# rooms = [
#     {'id':1, 'name':'Let learn Python'},
#     {'id':2, 'name':'Let learn RestFramework'},
#     {'id':3, 'name':'Let learn Django'},
#     {'id':4, 'name':'Let learn React'},
#     {'id':5, 'name':'Let learn PHP'},
# ]    