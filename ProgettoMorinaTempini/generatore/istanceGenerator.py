from generatore.gridGenerator import generaGriglia
from generatore.graphGenerator import generaGrafoDaGriglia
from generatore.pathGenerator import generaPaths
from generatore.pathGenerator import generaPathsReachGoal
from models.istanza import Istanza
import random

from IO.IO import run as plot

def initrandom(cellelibere):
    """Metodo per la generazione di una cella init random
    Parametri: lista cellelibere
    Restituisce: init"""
    init = random.choice(cellelibere)
    cellelibere.remove(init)
    return init

def goalrandom(cellelibere, init):
    """Metodo per la generazione di una cella goal random
    Parametri: lista cellelibere, cella init
    Restituisce: goal"""
    goal = random.choice(cellelibere)
    while goal == init:
        goal = random.choice(cellelibere)
    cellelibere.remove(goal)
    return goal
    

def creaInits(nagents, cellelibere): 
    """
    Metodo per la generazione di una lista di n celle init e della coppia (init,goal) per l'entry agent
    Parametri: numero di agenti, lista cellelibere
    Restituisce: inits, goalinit
    
    scegliamo n inizi random per gli n agenti (tutti gli init diversi tra loro), 
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
    """
    Metodo per la generazione di una dizionario contenente goal e init per ogni agente (goal è la chiave, init il valore), 
    compreso l'entry agent
    Parametri: numero di agenti, lista cellelibere
    Restituisce: goalsinits
    
    scegliamo randomicamente un init e un goal (diversi tra loro) per tutti gli n+1 agenti"""
    goalsinits={}
    for _ in range(nagents+1):
        init=initrandom(cellelibere)
        goal=goalrandom(cellelibere, init)
        goalsinits[goal]=init
    return goalsinits

def generaIstanza(nrwos, ncols, freeCellRatio, agglomerationFactor, nagents, usaReachGoal, limiteLunghezzaPathsEsistenti, maxOrizzonteTemporale, usaRilassato):
    """Metodo per la generazione dell'intera istanza
    Parametri: numero righe, numero colonne, ratio celle libera, fattore di aggregazione, numero di agenti, uso reachGoal, limite lunghezza paths esistenti, maxOrizzonteTemporale, uso rilassato
    Restituisce: Istanza, lista lunghezzePathsEsistenti, lista paths, initAgente, goalAgente

    Viene generata la griglia e successivamente il grafo. Dopodichè, se la configurazione lo consente, vengono generati i paths con il metodo indicato.
    """
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