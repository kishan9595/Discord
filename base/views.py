from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user is not valid.')  

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'username or password not exist.')     
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
           user = form.save(commit=False)
           user.username = user.username.lower()
           user.save()
           login(request, user)
           return redirect('home')
        else:
            messages.error(request, 'Error occured during registration')

    context = {'form':form}
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # rooms = Room.objects.filter(topic__name__icontains=q) or Room.objects.filter(name__icontains=q) or Room.objects.filter(content__icontains=q)
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(content__icontains=q)
        )

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_message = Message.objects.all()
    print(request.user)


    context = {'rooms': rooms, 'topics':topics, 'room_count':room_count, 'room_message':room_message}
    return render(request, 'base/home.html', context)

def room(request, pk):
    # print(request.user)
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)


    context = {'room': room, 'room_messages':room_messages, 'participants':participants}        
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html', context)    

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed Here')

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
           form.save()
        return redirect('home')
            
    context = {'form':form}
    return render(request, 'base/room_form.html', context) 

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed Here')

    if request.method == "POST":
        room.delete()
        return redirect('home')

    context = {'obj': room}
    return render(request, 'base/delete.html', context) 

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed Here')

    if request.method == "POST":
        message.delete()
        return redirect('home')

    context = {'obj':message}
    return render(request, 'base/delete.html', context) 




















# rooms = [
#     {'id':1, 'name':'Let learn Python'},
#     {'id':2, 'name':'Let learn RestFramework'},
#     {'id':3, 'name':'Let learn Django'},
#     {'id':4, 'name':'Let learn React'},
#     {'id':5, 'name':'Let learn PHP'},
# ]    