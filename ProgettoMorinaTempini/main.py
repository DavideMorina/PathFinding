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
    """Metodo per la lettura dei parametri: default, da file o da console"""
    if(len(sys.argv) == 1):
        print("Utilizzati parametri di default")
        rows=45
        col=45
        freeCellRatio=0.7
        fattore_agglomerazione=0.2
        nagents=40
        limiteLunghezzaPathsEsistenti=50
        usaReachGoal=True
        maxOrizzonteTemporale=60
        usaRilassato=False
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

def randomTesting():
    """Metodo per far comportare le generazioni random in un modo deterministico -> ci permette di rigenerare le stesse istanze"""
    seed = 8
    random.seed(seed)
    np.random.seed(seed)


def main():
    if(len(sys.argv)>1 and sys.argv[1]=="-test"):
        print("Modo testing attivo.")
        eseguiTest()
    else:
        #lettura parametri da terminale o da file
        rows, col, freeCellRatio, fattore_agglomerazione, nagents, usaReachGoal, limiteLunghezzaPathsEsistenti, maxOrizzonteTemporale, usaRilassato = letturaParametri()

        #opzionale: impostare un seed al random
        #randomTesting()

        #inizializzazione raccoglitore info
        info = raccoglitoreInfo()
        info.iniziaMonitoraggio()

        #inizializzazione istanza
        istanza, lunghezzePathsEsistenti, paths, initAgente, goalAgente = istanceGenerator.generaIstanza(rows, col, freeCellRatio, fattore_agglomerazione, nagents, usaReachGoal, limiteLunghezzaPathsEsistenti, maxOrizzonteTemporale, usaRilassato)
        if not istanza:
            print("Generazione istanza non riuscita.")
            sys.exit(1)


        #risoluzione istanza: calcolo path agente n+1
        pathAgente, contatoreOpen, contatoreClosed = reachGoal(istanza.getGrafo(), paths, initAgente, goalAgente, maxOrizzonteTemporale, usaRilassato)
        if not pathAgente:
            print("Impossibile trovare path per l'agente n+1.")
            sys.exit(1)
        paths.append(pathAgente)

        costoPathAgente = pathAgente.calcolaCosto()

        info.terminaMonitoraggio()
        info.setValori(istanza, freeCellRatio, fattore_agglomerazione, nagents, usaReachGoal, usaRilassato, limiteLunghezzaPathsEsistenti, lunghezzePathsEsistenti, maxOrizzonteTemporale, initAgente, goalAgente, pathAgente.getLunghezza(), costoPathAgente, pathAgente, contatoreOpen, contatoreClosed)
        info.scriviInfoSuFile() 
        info.printInfo()

        plot(istanza.getGriglia(), paths)

if __name__ == "__main__":
    main()