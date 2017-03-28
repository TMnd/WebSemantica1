"""
Definition of views.
"""
import csv
import sys

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.simpleGraph import simpleGraph
from app.forms import addTripleStore
from app.forms import removeTripleStore
from pathlib import Path
from graphviz import Source

sg = simpleGraph()
my_file = Path("triplos.csv")
if my_file.is_file():
    print("A dar load ao ficheiro...")
    sg.load("triplos.csv")
else: 
    print("O ficheiro nao foi encontrado")

print("Load efectuado!")

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'Sobre',
            'message':'Trabalho pratico para o ambito da disciplina de Web Semantica do Mestrado de Engenharia de Informatica',
            'year':datetime.now().year,
        }
    )

#para a pagina de grafos
def triples2dot(triples):
    dot = \
"""
graph "SimpleGraph" {
overlap = "scale";
"""
    for s, o, p in triples:  
        dot = dot + '"%s" -- "%s" [label="%s"]\n' % (s, o, p)
    dot = dot + "}"
    return dot

def createGraph(predicado):
    ts = sg.triples(None,predicado, None)
    dot = triples2dot(ts)
    g = Source(dot,format="png", engine="neato")    
    g.render('app/static/app/images/' + predicado + '.gv', view=False)
    print("Grafo criado")

def grafos(request):
    assert isinstance(request, HttpRequest)
    if 'grafo' in request.POST :
        predicado_escolhido = request.POST['grafo1']
        createGraph(predicado_escolhido)
        url= 'app/images/' + predicado_escolhido + '.gv.png'
        return render(request,'app/graph.html',{'url': url,'title':'Gerador de grafos',})
    else:
        return render(request,'app/graph.html',{'title':'Gerador de grafos',})

#Pagina das operações
def teste(request):
    """Pagina de inserir dados na triple store"""
    assert isinstance(request, HttpRequest)
    removeform = removeTripleStore()
    form = addTripleStore()
    if request.method == 'POST':
        if 'inserirDados' in request.POST:
            form = addTripleStore(request.POST)
            lista = []
            if form.is_valid():
                Sujeito = request.POST.get('Sujeito','')
                Predicado = request.POST.get('Predicado','')
                Objecto = request.POST.get('Objecto','')
            sg.add(Sujeito,Predicado,Objecto)
            generador = sg.listaTriplos()
            for i in generador:
                lista.append(i)
            return render(request, 'app/teste.html', {'removeform':removeform,'form': form,'Sujeito':Sujeito, 'Predicado':Predicado, 'Objecto':Objecto, 'titleDados':'Lista de triplos','listaTriplos':lista, 'titleLista':'Lista de triplos na triple store','titleInserirDados':'Inserir dados para a triple store', 'titleEliminarDados':'Eliminar tiplos'})
        elif 'removerDados' in request.POST:
            removeform = removeTripleStore(request.POST)
            lista = []
            if removeform.is_valid():
                rsujeito = request.POST.get('sujeito','')
                rpredicado = request.POST.get('predicado','')
                robjecto = request.POST.get('objecto','')

            sg.remove(rsujeito,rpredicado,robjecto)
            generador = sg.listaTriplos()
            for i in generador:
                lista.append(i)

            return render(request, 'app/teste.html', {'listaTriplos':lista,'form': form,'removeform':removeform,'Sujeito':rsujeito, 'Predicado':rpredicado, 'Objecto':robjecto, 'titleDados':'Lista de triplos','listaTriplos':lista, 'titleLista':'Lista de triplos na triple store','titleInserirDados':'Inserir dados para a triple store', 'titleEliminarDados':'Eliminar tiplos da triple store'})
    else:
        lista = []    
        form = addTripleStore()
        removeform = removeTripleStore()

        #Para listar todos os conteudos da triple store
        generador = sg.listaTriplos()
        for i in generador:
            lista.append(i)
        return render(request, 'app/teste.html', {'form': form, 'removeform':removeform, 'titleLista':'Lista de triplos na triple store','titleInserirDados':'Inserir dados para a triple store', 'titleEliminarDados':'Eliminar tiplos da triple store','listaTriplos':lista})
