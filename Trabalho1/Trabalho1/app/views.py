"""
Definition of views.
"""
import csv
import sys

from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import RequestContext
from datetime import datetime
from app.simpleGraph import simpleGraph
from app.forms import addTripleStore
from app.forms import removeTripleStore
from app.forms import pesquisarTripleStore
from app.inferencerule import *
from pathlib import Path
from graphviz import Source
import operator


#x = simpleGraph()
sg = simpleGraph()

my_file = Path("triplos.csv")
if my_file.is_file():
    print("A dar load ao ficheiro...")
    #x.load("triplos.csv")
    sg.load("triplos.csv")
else: 
    print("O ficheiro nao foi encontrado")

#Inferences
g = routRule()
sg.applyinference(g)


def classificacao(request):
    assert isinstance(request, HttpRequest)

    equipas = []
    for i in sg.triples(None, 'HomeTeam', None):
        if i[2] not in equipas:
            equipas.append(i[2])

    dataset = []
    for i in sg.triples(None, 'HomeTeam', None):
        dataset.append(i)
    for i in sg.triples(None, 'AwayTeam', None):
        dataset.append(i)
    for i in sg.triples(None, 'FTHG', None):
        dataset.append(i)
    for i in sg.triples(None, 'FTAG', None):
        dataset.append(i)
    for i in sg.triples(None, 'FTR', None):
        dataset.append(i)

    ids = []
    for j in sg.triples(None, 'HomeTeam', None):
        ids.append(j[0])

    jogos = {}
    for i in ids:
        estatisticas = []
        for j in dataset:
            if i == j[0]:
                estatisticas.append(j[2])
        jogos[i] = estatisticas

    equipas = {}
    for i in jogos:
        if jogos[i][0] not in equipas:
            equipas[jogos[i][0]] = [0, 0, 0, 0, 0, 0, 0]  #pontos, vitorias, empates, derrotas, golos marcados, golos sofridos, diferença de golos

        if jogos[i][2] > jogos[i][3]:  # casa > fora
            for j in equipas:

                if jogos[i][0] == j:  # casa
                    equipas[j][0] += 3  # casa +3 pontos
                    equipas[j][1] += 1  # nº vitorias casa

                    equipas[j][4] += int(jogos[i][2])  # golos marcados pela equipa da casa
                    equipas[j][5] += int(jogos[i][3])  # golos sofridos pela equipa da casa

                if jogos[i][1] == j:  # fora
                    equipas[j][3] += 1  # nº derrotas fora

                    equipas[j][4] += int(jogos[i][3])  # golos marcados pela equipa da fora
                    equipas[j][5] += int(jogos[i][2])  # golos sofridos pela equipa da fora

        elif jogos[i][2] == jogos[i][3]:  # casa == fora
            for j in equipas:

                if jogos[i][0] == j:  # casa
                    equipas[j][0] += 1  # casa +1 ponto
                    equipas[j][2] += 1  # nº empates casa
                    equipas[j][4] += int(jogos[i][2])  # golos marcados pela equipa da casa
                    equipas[j][5] += int(jogos[i][3])  # golos sofridos pela equipa da casa

                if jogos[i][1] == j:  # fora
                    equipas[j][0] += 1  # fora +1 ponto
                    equipas[j][2] += 1  # nº empates fora

                    equipas[j][4] += int(jogos[i][3])  # golos marcados pela equipa da fora
                    equipas[j][5] += int(jogos[i][2])  # golos sofridos pela equipa da fora

        elif jogos[i][2] < jogos[i][3]:  # casa < away
            for j in equipas:

                if jogos[i][0] == j:  # casa
                    equipas[j][3] += 1  # nº derrotas casa

                    equipas[j][4] += int(jogos[i][2])  # golos marcados pela equipa da casa
                    equipas[j][5] += int(jogos[i][3])  # golos sofridos pela equipa da casa

                if jogos[i][1] == j:  # fora
                    equipas[j][0] += 3  # fora +3 pontos
                    equipas[j][1] += 1  # nº vitorias fora

                    equipas[j][4] += int(jogos[i][3])  # golos marcados pela equipa da fora
                    equipas[j][5] += int(jogos[i][2])  # golos sofridos pela equipa de fora

                equipas[j][6] = equipas[j][4] - equipas[j][5]  # diferença de golos

    equipas = sorted(equipas.items(), key=operator.itemgetter(1))
    posicoes = []
    for i in range(len(equipas)):
        posicoes.append(i+1)
    
    classificacao = []
    for i, j in zip(reversed(range(len(equipas))), posicoes):
        classificacao.append([j, equipas[i][0], equipas[i][1][0], equipas[i][1][1], equipas[i][1][2], equipas[i][1][3], equipas[i][1][4], equipas[i][1][5], equipas[i][1][6]])

    #print("Posição", "Equipa", "Pontos", "Vitórias", "Empates", "Derrotas", "Golos Marcados", "Golos Sofridos", "Diferença de Golos")
    #for i, j in zip(reversed(range(len(equipas))), posicoes):
            #print(j, equipas[i][0], equipas[i][1][0], equipas[i][1][1], equipas[i][1][2], equipas[i][1][3], equipas[i][1][4], equipas[i][1][5], equipas[i][1][6])


    return render(
        request, 
        'app/classificacao.html',
        {
        'classList':classificacao
        }
    )

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

def jogo(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    TeamsList = []
    NotSameTeam = False
    aux = False
    HomeTeam = None
    AwayTeam = None
    B365H = None
    B365D = None
    B365A = None
    BWH = None
    BWD = None
    BWA = None
    FTHG = None
    FTAG = None
    FTR = None
    Gols = False #para a goleada
    
    teams = sg.query([('?id_jogo','HomeTeam','?TeamName')])
    for TeamName in teams:
        team = TeamName.get("TeamName")
        TeamsList.append(team)

    TeamsList = sorted(set(TeamsList))
    print(TeamsList)

    assert isinstance(request, HttpRequest)
    if 'game' in request.POST :
        HomeTeam = request.POST['hometeam']
        AwayTeam = request.POST['awayteam']
        
        print(HomeTeam)
        print(AwayTeam)

        if HomeTeam==AwayTeam:
            NotSameTeam = True
        else:
            aux = True

        gameInformation = sg.query([('?id_jogo','HomeTeam',HomeTeam),
                                   ('?id_jogo','AwayTeam',AwayTeam),
                                   ('?id_jogo','FTHG', '?GolsHome'),
                                   ('?id_jogo','FTAG', '?GolsAway'),
                                   ('?id_jogo','FTR', '?FinalResult'),
                                   ('?id_jogo','B365H','?WinHomeOddsB365'),
                                   ('?id_jogo','B365D','?DrawOddsB365'),
                                   ('?id_jogo','B365A','?WinAwayOddsB365'),
                                   ('?id_jogo', 'BWH', '?WinHomeOddsBW'),
                                   ('?id_jogo', 'BWD', '?DrawOddsBW'),
                                   ('?id_jogo', 'BWA', '?WinAwayOddsBW')])

        print(str(gameInformation))

        for i in gameInformation:
            B365H = i.get('WinHomeOddsB365')
            print(B365H)
            B365D = i.get('DrawOddsB365')
            print(B365D)
            B365A = i.get('WinAwayOddsB365')
            print(B365A)
            BWH = i.get('WinHomeOddsBW')
            print(BWH)
            BWD = i.get('DrawOddsBW')
            print(BWD)
            BWA = i.get('WinAwayOddsBW')
            print(BWA)
            FTHG = i.get('GolsHome')
            print(FTHG)
            FTAG = i.get('GolsAway')
            print(FTAG)
            FTR = i.get('FinalResult')
            print(FTR)
            G = i.get('id_jogo')
            generator = sg.triples(G,'G', None)
            for ola in generator:
                Gols = True  #se existir um triplo com o predicado G
        


    return render(request,'app/jogo.html',{'title':'Game','message':'Chose the teams','teamlist':TeamsList,'NotSameTeam':NotSameTeam,'aux':aux,'HomeTeam':HomeTeam,'AwayTeam':AwayTeam,'B365H':B365H,'B365D':B365D,'B365A':B365A,'BWH':BWH,'BWD':BWD,'BWA':BWA,'FTHG':FTHG,'FTAG':FTAG,'FTR':FTR,'Gols':Gols})

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
    pesquisarform = pesquisarTripleStore()
    if request.method == 'POST':
        if 'inserirDados' in request.POST:
            form = addTripleStore(request.POST)
            lista = []
            listaPesquisa = []
            if form.is_valid():
                Sujeito = request.POST.get('Sujeito','')
                Predicado = request.POST.get('Predicado','')
                Objecto = request.POST.get('Objecto','')
            sg.add(Sujeito,Predicado,Objecto)
            generador = sg.listaTriplos()
            for i in generador:
                lista.append(i)
            return render(request, 'app/teste.html', {'removeform':removeform,'form': form,'Sujeito':Sujeito, 'Predicado':Predicado, 'Objecto':Objecto, 'listaPesquisa':listaPesquisa,'titleDados':'Lista de triplos','listaTriplos':lista, 'titleLista':'Lista de triplos na triple store','titleInserirDados':'Inserir dados para a triple store', 'titleEliminarDados':'Eliminar tiplos da triple store','titlePesquisarDados':'Pesquisar triplos'})
        elif 'removerDados' in request.POST:
            removeform = removeTripleStore(request.POST)
            lista = []
            listaPesquisa = []
            if removeform.is_valid():
                rsujeito = request.POST.get('sujeito','')
                rpredicado = request.POST.get('predicado','')
                robjecto = request.POST.get('objecto','')
            sg.remove(rsujeito,rpredicado,robjecto)
            generador = sg.listaTriplos()
            for i in generador:
                lista.append(i)

            return render(request, 'app/teste.html', {'listaTriplos':lista,'form': form,'removeform':removeform,'Sujeito':rsujeito, 'Predicado':rpredicado, 'Objecto':robjecto, 'listaPesquisa':listaPesquisa, 'titleDados':'Lista de triplos','listaTriplos':lista, 'titleLista':'Lista de triplos na triple store','titleInserirDados':'Inserir dados para a triple store', 'titleEliminarDados':'Eliminar tiplos da triple store', 'titlePesquisarDados':'Pesquisar triplos'})
        elif 'pesquisarDados' in request.POST:
            pesquisarform = pesquisarTripleStore(request.POST)
            lista = []
            
            listaPesquisa = []
            #if pesquisarform.is_valid():
            psujeito = request.POST.get('sujeito','')
            ppredicado = request.POST.get('predicado','')
            pobjecto = request.POST.get('objecto','')
            
            if len(psujeito)==0:
                psujeito = None
            if len(ppredicado)==0:
                ppredicado = None
            if len(pobjecto)==0:
                pobjecto = None
            pesquisa_gerador = sg.triples(psujeito,ppredicado,pobjecto)
            for i in pesquisa_gerador:
                #print(i)
                listaPesquisa.append(i)
            generador = sg.listaTriplos()
            for i in generador:
                #print(i)
                lista.append(i)
            return render(request, 'app/teste.html', {'listaTriplos':lista,'form': form,'removeform':removeform,'Sujeito':psujeito, 'Predicado':ppredicado, 'Objecto':pobjecto, 'listaPesquisa':listaPesquisa,'titleDados':'Lista de triplos','listaTriplos':lista, 'titleLista':'Lista de triplos na triple store','titleInserirDados':'Inserir dados para a triple store', 'titleEliminarDados':'Eliminar tiplos da triple store', 'titlePesquisarDados':'Pesquisar triplos'})
    else:
        lista = []
        listaPesquisa = []
        form = addTripleStore()
        removeform = removeTripleStore()
        pesquisarform = pesquisarTripleStore(initial={'psujeito': 'ola','sujeito':'ols','Sujeito':'ole'})
        #Para listar todos os conteudos da triple store
        generador = sg.listaTriplos()
        for i in generador:
            lista.append(i)
        return render(request, 'app/teste.html', {'form': form, 'removeform':removeform, 'listaPesquisa':listaPesquisa, 'titleLista':'Lista de triplos na triple store','titleInserirDados':'Inserir dados para a triple store', 'titleEliminarDados':'Eliminar tiplos da triple store','listaTriplos':lista, 'titlePesquisarDados':'Pesquisar triplos'})