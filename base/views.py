from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import Message, Room, Topic
from .forms import RoomForm, UserForm
# Create your views here.

# rooms=[
#    { 'id':1, 'name':'Lests learn python!'},
#    { 'id':2, 'name':'Design whith me!'},
#    { 'id':3, 'name':'Frontend development'},

# ]

#dar(retrieve) um objeto especifico
#queryi = Modelname.objects.get(Atribute -'value)

# filter(attribte -='value') - retorna todos os itemas da tabela que correspondem ao atributo

def loginPage(request):

    page='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        #scripst para processar os inputs pelo forma.py, valida-los e salva-los
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user =User.objects.get(username=username)
        except:
            messages.error(request, 'Usuario não existe!!')

        #autenticacao do user, se existe retona um objeto, se nao um erro
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Senha nao existem')


    context={'page':page}
    return render(request, 'base/login_register.html', context)




def logoutUser(request):
    
    logout(request)
    return redirect('home')


def registerPage(request):
    # page = 'register'
    form = UserCreationForm()

    if request.method =='POST':
        # request.POST -> informacoes enviadas no estado atual(senha e usuario)

        form = UserCreationForm(request.POST)
        if form.is_valid():
            #commit=False -> "freeze " salvamento no estado para fazer alteraçõess
            user =form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Um erro ocorreu durante o registro!')

    return render(request,'base/login_register.html', {'form':form})


def home(request):
    #inline icontains
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    #pesquisas estatica
    # rooms = Room.objects.filter(topic__name__icontains = q)

    #pesquisa dinamica com o django.db.models import Q
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q)|
        
        Q(name__icontains = q)|
        Q(description__icontains = q)
    
    )
    #icontains outras opcoes= starwith, endwith etc

    # # get tosdos os rooms do database
    # rooms = Room.objects.all()

    topics = Topic.objects.all()
    #lin method
    room_count =rooms.count()

     # <!-- COLUNA de atividades recentes -->
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rooms, 'topics':topics, 
               'room_count':room_count, 'room_messages':room_messages}
    return render(request,  'base/home.html', context)




def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    # room_messages = room.message_set.all().order_by('-created')
    
    #'coletar 'todos os participantes 
    participants = room.participants.all()
    #criar messagem/comentario
    if request.method =='POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        #adicionar participantes ao room que ele acessar
        room.participants.add(request.user)

        return redirect('room', pk=room.id)
    
    context ={'room': room, 'room_messages':room_messages,'participants':participants }
    return render(request,  'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    #rooms sao acessados assim no feed_component logo, vai ser aqui tambem
    context ={'user':user, 'rooms':rooms,
               'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)




#criar a funcao que ira criar o formulario dinamico e motrar no temaplete
@login_required(login_url = 'login')
def createRoom(request):
    form = RoomForm
    topics = Topic.objects.all()
    # oque fazer quando for POST ?
    if request.method =='POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        #scripst para processar os inputs pelo forma.py, valida-los e salva-los
        form = RoomForm(request.POST)


        Room.objects.create(
            host = request.user,
            topic = topic,
            name= request.POST.get('name'),
            description= request.POST.get('description'),

        )
        # if form.is_valid():
        #     room = form.save(commit=False)

            
        #     #colocar o usuaro que esta criando o room como o host dele
        #     room.host = request.user
        #     room.save()
        #     #posso usar o 'home' pq tem a tag name= no urls
        return redirect('home')
    
        # print(request.POST)
        #request.POST.get('name')
    context ={'form':form , 'topics':topics}
    return render(request, 'base/room_form.html', context)





def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    ##veja que o instance, instancia o room exato que queremos atualizar, !!important
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host :
        return HttpResponse('Voce nao tem permissao aqui!!')


    if request.method =='POST':
    #scripst para processar os inputs pelo forma.py, valida-los e salva-los
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
    
            #posso usar o 'home' pq tem a tag name= no urls
        return redirect('home')
        # print(request.POST) #--> para printar oque foi escrito no forms
        #request.POST.get('name')

    #dicionarionpara sinplificar a entrada do render
    context={'form':form, 'topics':topics, 'room':room}
    return render(request,  'base/room_form.html', context)



@login_required(login_url ='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    #se for post metod = clicou em deletar, confirm form
    if request.user != room.host :
        return HttpResponse('Voce nao tem permissao aqui!!')

    if request.method =='POST':
    #scripst para processar os inputs pelo forma.py, valida-los e salva-los
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url ='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    #se for post metod = clicou em deletar, confirm form
    if request.user != message.user:
        return HttpResponse('Voce nao tem permissao aqui!!')

    if request.method =='POST':
    #scripst para processar os inputs pelo forma.py, valida-los e salva-los
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user =request.user
    form =UserForm(instance = user)

    if request.method =='POST':
        form =UserForm(request.POST, instance=user )
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form':form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') !=None else ''
    topics = Topic.objects.filter()
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html',{'room_messages':room_messages})

