from .euristica import calcolaEuristica
from .reconstructPath import reconstructPath
from .calcolaPianoRilassato import calcolaPianoRilassato
import math

from collections import OrderedDict


def reachGoal(grafo, paths, init, goal, maxOrizzonteTemporale, usaRilassato=False):
    """calcola un percorso tra init e goal"""

    #stato si riferisce a coppia (vertice,tempo)
    closedList=[] #lista degli stati già espansi
    openList=[(init,0)] #lista di stati da espandere
    contatoreOpen=0

    parentDict = {} #chiave: coppia (vertice,tempo), valore: coppia (vertice tempo) genitore
    gDict = {} #chiave: coppia (vertice,tempo), valore: valore di g(vertice,tempo)

    """for t in range(maxOrizzonteTemporale+1):
        for vertice in grafo.getNodi():
            gDict[(vertice,t)]=math.inf"""
            #p -> nil
    
    gDict[(init,0)] = 0
    euristica = calcolaEuristica(grafo, goal) #hash di euristiche, chiave: coppia (vertice,goal), valore: h(vertice,goal)

    fDict = {} #chiave: coppia(vertice,tempo), valore: g(vertice,goal)+h(vertice,goal)
    fDict[(init, 0)] = euristica[(init, goal)]   

    while (len(openList)>0):
        #stato con f minore
        current = min(openList, key=lambda x: fDict[x]) #current è l'elemento della openList con il rispettivo valore di f minore
        tempo = current[1]
        verticeCurrent = current[0]
        openList.remove(current)
        closedList.append(current)
        if (verticeCurrent == goal):
            return reconstructPath(init,goal,parentDict,tempo, 0), contatoreOpen, len(closedList)
        
        #Condizione terminazione rilassato
        if(usaRilassato):
            pathRilassato = calcolaPianoRilassato(verticeCurrent, goal, grafo, tempo, maxOrizzonteTemporale)
            if(pathRilassato is not None):
                # for p in paths:
                #     if(p.isMossaIllegale(pathRilassato.getMossa(tempo), pathRilassato.getMossa(tempo+1), tempo)):
                if(collisionFree(paths, pathRilassato, tempo, goal)):
                    print("AAAAAAAAAAAAAAA")
                    print(verticeCurrent)
                    return combinaPaths(pathRilassato, reconstructPath(init, verticeCurrent, parentDict, tempo, 0)), contatoreOpen, len(closedList)

        if (tempo < maxOrizzonteTemporale):
            for arco in grafo.getVicini(verticeCurrent):
                nodo=arco.dest
                peso=arco.peso
                nextTempo = tempo + 1
                if((nodo,nextTempo) not in closedList):
                    attraversabile = True
                    for percorsoPrecedente in paths: #checkIllegalMove
                        if(percorsoPrecedente.isMossaIllegale(verticeCurrent, nodo, tempo, goal)):
                            attraversabile = False
                    if(attraversabile):
                        setdefault_g(gDict, (nodo, nextTempo), float('inf'))
                        #gDict[(nodo, nextTempo)]=math.inf  #inizializzo gDict
                        if(gDict[(verticeCurrent, tempo)] + peso < gDict[(nodo, nextTempo)]):
                            parentDict[(nodo, nextTempo)] = (verticeCurrent, tempo)
                            gDict[(nodo, nextTempo)] = gDict[(verticeCurrent, tempo)] + peso
                            fDict[(nodo, nextTempo)] = gDict[(nodo, nextTempo)] + euristica[(nodo, goal)]
                        if((nodo, nextTempo) not in openList):
                            openList.append((nodo, nextTempo))  
                            contatoreOpen+=1   

    return None, None, None #se non è possibile raggiungere il goal

def collisionFree(paths, pathRilassato, tempo, goal):
    for p in paths:
        t = tempo
        for mossa in pathRilassato.getMosse():
            if(p.isMossaIllegale(mossa[1].getOrig(), mossa[1].getDst(), t, goal)):
                return False
            t += 1
    return True

def combinaPaths(pathRilassato, pathReconstruct):
    #aggiunta delle mosse del pathRilassato alla fine del pathReconstruct
    pathReconstruct.invertiMosse() #ordiniamo mosse path parziale costruito con reachgoal classico
    for mossa in pathRilassato.getMosse(): 
        #print(mossa)
        pathReconstruct.addMossa(mossa[0], mossa[1])
    pathReconstruct.setGoal(pathRilassato.getGoal()) #settiamo il goal del path composto
    return pathReconstruct

def setdefault_g(dizionario, chiave, valore_predefinito):
    if chiave not in dizionario:
        dizionario[chiave] = valore_predefinito
    return dizionario[chiave]