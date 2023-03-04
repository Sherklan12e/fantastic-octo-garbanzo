from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Publicacion, Comentario
from .forms import PublicacionForm
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from .models import User
from .forms import RegisterUserForm


def publicacion_lista(request):
    publicaciones = Publicacion.objects.all().order_by('-fecha_creacion')
    return render(request, 'publicacion_lista.html', {'publicaciones': publicaciones})

@login_required(login_url='login')
def publicacion_nueva(request):
    if request.method == "POST":
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.autor = request.user
            publicacion.save()
            messages.success(request, 'Publicación publicada!')
            return redirect('publicacion_detalle', pk=publicacion.pk)
    else:
        form = PublicacionForm()
    return render(request, 'publicacion_editar.html', {'form': form})

def publicacion_detalle(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    comentarios = publicacion.comentarios.all().order_by('-fecha_creacion')
    if request.method == "POST":
        autor = request.POST.get('autor', None)
        correo = request.POST.get('correo', None)
        mensaje = request.POST.get('mensaje', None)
        Comentario.objects.create(publicacion=publicacion, autor=autor, correo=correo, mensaje=mensaje)
        return redirect('publicacion_detalle', pk=publicacion.pk)
    return render(request, 'publicacion_detalle.html', {'publicacion': publicacion, 'comentarios': comentarios})

@login_required
def publicacion_editar(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if request.method == "POST":
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.autor = request.user
            publicacion.save()
            return redirect('publicacion_detalle', pk=publicacion.pk)
    else:
        form = PublicacionForm(instance=publicacion)
    return render(request, 'publicacion_editar.html', {'form': form})

@login_required
def publicacion_borrar(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    publicacion.delete()
    return redirect('publicacion_lista')



def register_page(request):
    form = RegisterUserForm()
    
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            
            login(request, user)
            messages.success(request, "Account created!")
            return redirect('home')
        else:
            messages.success(request, "a error ocorred during ")
    return render(request, "register.html", {'form':form})


def logout_user(request):
    logout(request)
    messages.success(request, "NOS VEMOS DESPUES prrr")
    return redirect("login")



def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
        except:
            messages.success(request, "User does not exist!")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "WELCOME BACK " + user.email)
            return redirect('home')
        else:
            messages.success(request, "USERNAME OR PASSWORD DOES NOT MATCH!")
            
    return render(request, "login.html")

