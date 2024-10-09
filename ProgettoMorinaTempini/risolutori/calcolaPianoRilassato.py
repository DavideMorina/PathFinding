from .euristica import calcolaEuristica
from models.path import Path
from models.path import Mossa
def calcolaPianoRilassato(vertice, goal, grafo, tempo, maxOrizzonteTemporale):
    path = Path(vertice, goal)
    current=vertice
    t=tempo
    euristica = calcolaEuristica(grafo, goal)
    while(current!=goal):
        if(t>=maxOrizzonteTemporale): return None
        nodo=None
        for arco in grafo.getVicini(current): #seleziono tra i vicni il nodo con migliore euristica
            if(nodo==None): 
                nodo=arco.dest
                peso=arco.peso
            else: 
                if(euristica[(nodo, goal)] > euristica[(arco.dest, goal)]):
                    nodo = arco.dest
                    peso = arco.peso
        path.addMossa(t, Mossa(current, nodo, peso))
        t += 1
        current = nodo
	
    return path