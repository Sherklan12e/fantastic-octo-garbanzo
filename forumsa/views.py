from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Publicacion, Comentario
from .forms import PublicacionForm
from django.contrib import messages 
def publicacion_lista(request):
    publicaciones = Publicacion.objects.all().order_by('-fecha_creacion')
    return render(request, 'publicacion_lista.html', {'publicaciones': publicaciones})

@login_required
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
