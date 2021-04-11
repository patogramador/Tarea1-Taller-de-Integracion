from django.urls import path

from . import views

app_name = "temporadas"
urlpatterns = [
    path('', views.index, name='index'),
    path('episodio/<str:id_episodio>/', views.episodio, name='episodio'),
    path('personaje/<str:nombre>/', views.personaje, name='personaje'),
    path('busqueda/', views.busqueda, name='busqueda'),
    path('<str:serie>/<str:id_temporada>/', views.temporada, name='temporada'),
]