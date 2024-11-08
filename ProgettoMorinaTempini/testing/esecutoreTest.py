import generatore.istanceGenerator as istanceGenerator
from testing.raccoglitoreInfoTest import raccoglitoreInfoTest
from risolutori.reachGoal import reachGoal
from generatore.gridGenerator import generaGriglia
from generatore.graphGenerator import generaGrafoDaGriglia
from generatore.pathGenerator import generaPaths
from generatore.pathGenerator import generaPathsReachGoal
from models.istanza import Istanza
import sys
import json
import random
import numpy as np
from IO.IO import run as plot

def letturaParametri():
    """Metodo per la lettura dei parametri da un file json"""
    with open('input.json', 'r') as file:
        # Carica il contenuto del file come un dizionario Python
        dati = json.load(file)

    # Accesso ai dati
    rows = dati['rows']
    col = dati['columns']
    freeCellRatio = dati['freeCellRatio']
    fattore_agglomerazione = dati['agglomerationFactor']
    nagents=dati['nagents']
    limiteLunghezzaPathsEsistenti=dati['limiteLunghezzaPathsEsistenti']
    if(dati['usareReachGoalAgentiPreesistenti']=="False"):
        usaReachGoal=False
    else: usaReachGoal=True
    maxOrizzonteTemporale=dati['maxOrizzonteTemporale']
    if(dati['usaRilassato']=="False"):
        usaRilassato=False
    else: usaRilassato=True
    
    return int(rows), int(col), float(freeCellRatio), float(fattore_agglomerazione), int(nagents), usaReachGoal, int(limiteLunghezzaPathsEsistenti), int(maxOrizzonteTemporale), usaRilassato

def randomTesting():
    """Metodo per far comportare le generazioni random in un modo deterministico -> ci permette di rigenerare le stesse istanze"""
    seed = 21
    random.seed(seed)
    np.random.seed(seed)

def testingIstanza(info, rows, cols, freeCellRatio, fattore_agglomerazione, nagents, usaReachGoal, limiteLunghezzaPathsEsistenti, maxOrizzonteTemporale, usaRilassato):
    """Metodo per la generazione dell'istanza in modalità test

    Parametri: raccoglitoreInfoTest info, rows, cols, freeCellRatio, fattore_agglomerazione, nagents, usaReachGoal, limiteLunghezzaPathsEsistenti, maxOrizzonteTemporale, usaRilassato 
    Restituisce: Istanza, lista lunghezzePathsEsistenti, lista paths, initAgenteReach, goalAgenteReach

    Viene generata la griglia e successivamente il grafo. 
    Dopodichè, se la configurazione lo consente, vengono generati i paths con il metodo indicato.
    Per ogni sezione vengono monitorate le prestazioni
    """

    info.iniziaMonitoraggioGrigliaGrafo()
    griglia = generaGriglia(rows, cols, freeCellRatio, fattore_agglomerazione)
    grafo = generaGrafoDaGriglia(griglia)
    info.terminaMonitoraggioGrigliaGrafo()

    #path
    cellelibere=list(grafo.getNodi())
    if(len(cellelibere)<nagents):
        print("Non c'è abbastanza spazio per tutti gli agenti")
        return None, None, None, None, None

    # Generazione istanza pseudo random
    info.iniziaMonitoraggioGridPseudo()
    inits, goalinit = istanceGenerator.creaInits(nagents, cellelibere)
    pathsPseudo = generaPaths(inits, goalinit, nagents, limiteLunghezzaPathsEsistenti, grafo)
    if not pathsPseudo:
        print("Impossibile trovare un percorso per tutti gli agenti")
        return None, None, None, None, None
    chiaviPseudo=list(goalinit.keys())
    goalAgentePseudo=chiaviPseudo[0]
    initAgentePseudo=goalinit[goalAgentePseudo]
    info.terminaMonitoraggioGridPseudo()
    
    # generazione istanza con reach goal
    info.iniziaMonitoraggioGridReach()
    goalsinits = istanceGenerator.creaInitsReachGoal(nagents, cellelibere)
    pathsReach = generaPathsReachGoal(goalsinits, nagents, maxOrizzonteTemporale, grafo, usaRilassato) #generazione istanza con reachgoal senza rilassato, coì da generare
    if not pathsReach:
        print("Impossibile trovare un percorso per tutti gli agenti")
        return None, None, None, None, None
    chiaviReach=list(goalsinits.keys())
    goalAgenteReach=chiaviReach[0]
    initAgenteReach=goalsinits[goalAgenteReach]
    info.terminaMonitoraggioGridReach()


    if(usaReachGoal):
        #ritorniamo l'istanza che utilizza ReachGoal
        lunghezzePathsEsistenti=[]
        for path in pathsReach:
            lunghezzePathsEsistenti.append(path.getLunghezza())

        return Istanza(griglia, grafo), lunghezzePathsEsistenti, pathsReach, initAgenteReach, goalAgenteReach
    else:
        #ritorniamo l'istanza che utilizza generazione pseudo random
        lunghezzePathsEsistenti=[]
        for path in pathsPseudo:
            lunghezzePathsEsistenti.append(path.getLunghezza())
            
        return Istanza(griglia, grafo), lunghezzePathsEsistenti, pathsPseudo, initAgentePseudo, goalAgentePseudo

def eseguiTest():
    """Metodo per l'esecuzione del test
    
    Parametri: nessuno
    Restituisce: nessuno

    Esegue il test generando una griglia, generando il grafo, generando i paths e il percorso dell'entry agent.
    Il tutto è eseguito nelle varie modalità possibili, monitorando le prestazioni e scrivendo i risultati su file.
    """
    rows, col, freeCellRatio, fattore_agglomerazione, nagents, usaReachGoal, limiteLunghezzaPathsEsistenti, maxOrizzonteTemporale, usaRilassato = letturaParametri()

    randomTesting()

    info = raccoglitoreInfoTest()

    #TESTING ISTANZA
    istanza, lunghezzePathsEsistenti, paths, initAgente, goalAgente = testingIstanza(info, rows, col, freeCellRatio, fattore_agglomerazione, nagents, usaReachGoal, limiteLunghezzaPathsEsistenti, maxOrizzonteTemporale, usaRilassato)
    if not istanza:
            print("Generazione istanza non riuscita.")
            sys.exit(1)

    #RISOLUZIONE ISTANZA
    #REACHGOAL
    info.iniziaMonitoraggioReachGoal()
    pathAgenteReachGoal, contatoreOpenReachGoal, contatoreClosedReachGoal = reachGoal(istanza.getGrafo(), paths, initAgente, goalAgente, maxOrizzonteTemporale, False) #forziamo risoluzione con rilassato a false
    if not pathAgenteReachGoal:
        print("Impossibile trovare path per l'agente n+1.")
        sys.exit(1)
    info.terminaMonitoraggioReachGoal()

    #REACHGOAL RILASSATO
    info.iniziaMonitoraggioReachGoalRilassato()
    pathAgenteReachGoalRilassato, contatoreOpenReachGoalRilassato, contatoreClosedReachGoalRilassato = reachGoal(istanza.getGrafo(), paths, initAgente, goalAgente, maxOrizzonteTemporale, True) #forziamo risoluzione con rilassato a true
    if not pathAgenteReachGoalRilassato:
        print("Impossibile trovare path rilassato per l'agente n+1.")
        sys.exit(1)
    info.terminaMonitoraggioReachGoalRilassato()

    paths.append(pathAgenteReachGoal)
    paths.append(pathAgenteReachGoalRilassato)
    costoPathAgenteReachGoal= pathAgenteReachGoal.calcolaCosto()
    costoPathAgenteReachGoalRilassato = pathAgenteReachGoalRilassato.calcolaCosto()
    info.setValori(istanza, freeCellRatio, fattore_agglomerazione, nagents, usaReachGoal, usaRilassato, limiteLunghezzaPathsEsistenti, lunghezzePathsEsistenti, maxOrizzonteTemporale, initAgente, goalAgente, pathAgenteReachGoal.getLunghezza(), pathAgenteReachGoalRilassato.getLunghezza(), costoPathAgenteReachGoal, costoPathAgenteReachGoalRilassato, pathAgenteReachGoal, pathAgenteReachGoalRilassato, contatoreOpenReachGoal, contatoreOpenReachGoalRilassato, contatoreClosedReachGoal, contatoreClosedReachGoalRilassato)
    info.scriviInfoSuFile()

    plot(istanza.getGriglia(), paths)
    