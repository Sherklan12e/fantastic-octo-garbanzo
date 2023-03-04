from django.shortcuts import render
def hola(request):
    return render(request, 'index.html')

def videos(request):
    return render(request, 'videos.html')
def home(request):
    return render(request, 'home.html')



 

