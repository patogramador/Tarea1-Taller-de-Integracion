from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
import requests
# Create your views here.


def index(request):
    temporadas = {"BB": [], "BCS": []}
    r = requests.get("https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Better+Call+Saul")
    r = r.json()
    lista = []
    for ep in r:
        if ep["season"] not in lista:
            lista.append(ep["season"])
    temporadas["BCS"] = lista
    r = requests.get("https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Breaking+Bad")
    r = r.json()
    lista = []
    for ep in r:
        if ep["season"] not in lista:
            lista.append(ep["season"])
    temporadas["BB"] = lista
    return render(request, 'temporadas/index.html', temporadas)


def temporada(request, serie, id_temporada):
    lista = []
    if serie == "BB":
        r = requests.get("https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Breaking+Bad")
        r = r.json()
        for ep in r:
            if ep["season"] == id_temporada:
                lista.append({'id': ep["episode_id"], 'nombre': ep["title"]})
    else:
        r = requests.get("https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Better+Call+Saul")
        r = r.json()
        for ep in r:
            if ep["season"] == id_temporada:
                lista.append({'id': ep["episode_id"], 'nombre': ep["title"]})
    return render(request, 'temporadas/temporada.html', {'episodios': lista, 'serie': serie, 'temporada': id_temporada})


def episodio(request, id_episodio):
    r = requests.get(f"https://tarea-1-breaking-bad.herokuapp.com/api/episodes/{id_episodio}")
    r = r.json()
    r = r[0]
    fecha = r['air_date'].split("T")
    diccionario = {'id': r['episode_id'], 'nombre': r['title'], 'temporada': r['season'], 'fecha': fecha[0],
                   'numero': r['episode'], 'serie': r['series'], 'personajes': r['characters']}
    return render(request, 'temporadas/episodio.html', diccionario)


def personaje(request, nombre):
    sep = nombre.split(" ")
    nombre2 = "+".join(sep)
    r = requests.get(f"https://tarea-1-breaking-bad.herokuapp.com/api/characters?name={nombre2}")
    r = r.json()
    r = r[0]
    quotes = []
    r2 = requests.get(f"https://tarea-1-breaking-bad.herokuapp.com/api/quote?author={nombre2}")
    r2 = r2.json()
    for elem in r2:
        quotes.append(elem['quote'])
    diccionario = {'nombre': nombre, 'ocupacion': r['occupation'], 'imagen': r['img'], 'status': r['status'],
                   'nick': r['nickname'], 'BB': r['appearance'], 'actor': r['portrayed'],
                   'BCS': r['better_call_saul_appearance'], 'quotes': quotes}
    return render(request, 'temporadas/personaje.html', diccionario)


def busqueda(request):
    if request.method == 'GET':
        busqueda = request.GET.get('busqueda')
        r = requests.get(f"https://tarea-1-breaking-bad.herokuapp.com/api/characters?name={busqueda}")
        r = r.json()
        lista =[]
        for ch in r:
            lista.append(ch["name"])
        return render(request, 'temporadas/busqueda.html', {'nombres': lista, 'busqueda': busqueda})
