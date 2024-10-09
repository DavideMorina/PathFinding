from generatore.gridGenerator import generaGriglia
from generatore.graphGenerator import generaGrafoDaGriglia
from generatore.pathGenerator import generaPaths
from generatore.pathGenerator import generaPathsReachGoal
from models.istanza import Istanza
import random

from IO.IO import run as plot

def initrandom(cellelibere):
    init = random.choice(cellelibere)
    cellelibere.remove(init)
    return init

def goalrandom(cellelibere, init):
    goal = random.choice(cellelibere)
    while goal == init:
        goal = random.choice(cellelibere)
    cellelibere.remove(goal)
    return goal
    

def creaInits(nagents, cellelibere): 
    """scegliamo n inizi random per gli n agenti (tutti gli init diversi tra loro), 
    per l'n+1 agente scegliamo randomicamente un init ed un goal (diversi dagli altri)"""
    inits=set()
    for _ in range(nagents):
        init=initrandom(cellelibere)
        inits.add(init)

    #n+1 agente
    goalinit={} #hash: chiave=goal, valore=init
    init=initrandom(cellelibere)
    goal=goalrandom(cellelibere, init)
    goalinit[goal]=init
    
    return inits, goalinit

def creaInitsReachGoal(nagents, cellelibere):
    """scegliamo randomicamente un init e un goal (diversi tra loro) per tutti gli n+1 agenti"""
    goalsinits={}
    for _ in range(nagents+1):
        init=initrandom(cellelibere)
        goal=goalrandom(cellelibere, init)
        goalsinits[goal]=init
    return goalsinits

def generaIstanza(nrwos, ncols, freeCellRatio, agglomerationFactor, nagents, usaReachGoal, limiteLunghezzaPathsEsistenti, maxOrizzonteTemporale, usaRilassato):
    griglia = generaGriglia(nrwos, ncols, freeCellRatio, agglomerationFactor)
    grafo = generaGrafoDaGriglia(griglia)
    #grafo.printGrafo()

    #path
    cellelibere=list(grafo.getNodi())
    if(len(cellelibere)<nagents):
        print("Non c'è abbastanza spazio per tutti gli agenti")
        return None, None, None, None, None

    #generazione paths degli n agenti
    if(usaReachGoal):
        goalsinits = creaInitsReachGoal(nagents, cellelibere)
        paths = generaPathsReachGoal(goalsinits, nagents, maxOrizzonteTemporale, grafo, usaRilassato)
        if not paths:
            print("Impossibile trovare un percorso per tutti gli agenti")
            return None, None, None, None, None
        chiavi=list(goalsinits.keys())
        goalAgente=chiavi[0]
        initAgente=goalsinits[goalAgente]
    else:
        inits, goalinit = creaInits(nagents, cellelibere)
        paths = generaPaths(inits, goalinit, nagents, limiteLunghezzaPathsEsistenti, grafo)
        if not paths:
            print("Impossibile trovare un percorso per tutti gli agenti")
            return None, None, None, None, None
        chiavi=list(goalinit.keys())
        goalAgente=chiavi[0]
        initAgente=goalinit[goalAgente]

    lunghezzePathsEsistenti=[]
    for path in paths:
        #path.printPath()
        lunghezzePathsEsistenti.append(path.getLunghezza())

    #plot(griglia)

    return Istanza(griglia, grafo), lunghezzePathsEsistenti, paths, initAgente, goalAgente