import generatore.istanceGenerator as istanceGenerator
from raccoglitoreInfo import raccoglitoreInfo
from risolutori.reachGoal import reachGoal
from testing.esecutoreTest import eseguiTest
import sys
import json
import random
import numpy as np
from IO.IO import run as plot

def letturaParametri():
    if(len(sys.argv) == 1):
        print("Utilizzati parametri di default")
        rows=45
        col=45
        freeCellRatio=0.7
        fattore_agglomerazione=0.2
        nagents=40
        limiteLunghezzaPathsEsistenti=100
        usaReachGoal=False
        maxOrizzonteTemporale=150
        usaRilassato=True
    elif(sys.argv[1]=="-file"):
        print("Utilizzati parametri da file")

        # Apri il file JSON
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
        
    else:
        print("Utilizzati parametri passati da terminale")
        rows = sys.argv[1]
        col = sys.argv[2]
        freeCellRatio = sys.argv[3]
        fattore_agglomerazione = sys.argv[4]
        nagents = sys.argv[5]
        limiteLunghezzaPathsEsistenti = sys.argv[6]
        if(sys.argv[7]=="False"):
            usaReachGoal=False
        else: usaReachGoal=True
        maxOrizzonteTemporale = sys.argv[8]
        usaRilassato=sys.argv[9]


    return int(rows), int(col), float(freeCellRatio), float(fattore_agglomerazione), int(nagents), usaReachGoal, int(limiteLunghezzaPathsEsistenti), int(maxOrizzonteTemporale), usaRilassato

def randomTesting(usaRilassato):
    """Metodo per far comportare le generazioni random in un modo deterministico -> ci permette di rigenerare le stesse istanze"""
    seed = 2
    random.seed(seed)
    np.random.seed(seed)
    return False, usaRilassato


def main():
    #CELLA: coppia (colonna, riga) -> colonna = x, riga = y

    if(sys.argv[1]=="-test"):
        print("Modo testing attivo.")
        eseguiTest()
    else:
        #lettura parametri da terminale o da file
        rows, col, freeCellRatio, fattore_agglomerazione, nagents, usaReachGoal, limiteLunghezzaPathsEsistenti, maxOrizzonteTemporale, usaRilassato = letturaParametri()

        #SOLO PER TESTING:
        usaRilassato, veroUsaRilassato = randomTesting(usaRilassato)

        #inizializzazione raccoglitore info
        info = raccoglitoreInfo()
        info.iniziaMonitoraggio()

        #inizializzazione istanza
        istanza, lunghezzePathsEsistenti, paths, initAgente, goalAgente = istanceGenerator.generaIstanza(rows, col, freeCellRatio, fattore_agglomerazione, nagents, usaReachGoal, limiteLunghezzaPathsEsistenti, maxOrizzonteTemporale, usaRilassato)
        if not istanza:
            print("Generazione istanza non riuscita.")
            sys.exit(1)

        #SOLO PER TESTING
        usaRilassato=veroUsaRilassato


        #risoluzione istanza: calcolo path agente n+1
        pathAgente, contatoreOpen, contatoreClosed = reachGoal(istanza.getGrafo(), paths, initAgente, goalAgente, maxOrizzonteTemporale, usaRilassato)
        if not pathAgente:
            print("Impossibile trovare path per l'agente n+1.")
            sys.exit(1)
        #print("\nPath n+1-esimo agente: ")
        #pathAgente.printPath()
        paths.append(pathAgente)

        costoPathAgente = pathAgente.calcolaCosto()

        info.terminaMonitoraggio()
        info.setValori(istanza, freeCellRatio, fattore_agglomerazione, nagents, usaReachGoal, usaRilassato, limiteLunghezzaPathsEsistenti, lunghezzePathsEsistenti, maxOrizzonteTemporale, initAgente, goalAgente, pathAgente.getLunghezza(), costoPathAgente, pathAgente, contatoreOpen, contatoreClosed)
        info.scriviInfoSuFile() 
        info.printInfo()

        plot(istanza.getGriglia(), paths)

if __name__ == "__main__":
    main()