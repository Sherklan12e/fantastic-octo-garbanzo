
from django.urls import path
from .views import hola, videos, home
urlpatterns = [
    path('images/', hola, name="imagenes"),
    path('videos/', videos, name="videos"),
    path('', home, name="home"),
]
