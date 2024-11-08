from .euristica import calcolaEuristica
from .reconstructPath import reconstructPath
from .calcolaPianoRilassato import calcolaPianoRilassato
from .calcolaPianoRilassato import calcolaPianoRilassatoGreedy


def reachGoal(grafo, paths, init, goal, maxOrizzonteTemporale, usaRilassato=False):
    """Metodo contenente l'algoritmo risolutivo ReachGoal
    
    Parametri: grafo, paths, init, goal, maxOrizzonteTemporale, eventuale usaRilassato
    Restituisce: path, contatoreOpen, lunghezza closedList"""

    #stato si riferisce a coppia (vertice,tempo)
    closedList=[] #lista degli stati già espansi
    openList=[(init,0)] #lista di stati da espandere
    contatoreOpen=0

    parentDict = {} #chiave: coppia (vertice,tempo), valore: coppia (vertice tempo) genitore
    gDict = {} #chiave: coppia (vertice,tempo), valore: valore di g(vertice,tempo)
    
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
            #pathRilassato = calcolaPianoRilassatoGreedy(verticeCurrent, goal, grafo, tempo, maxOrizzonteTemporale)
            pathRilassato = calcolaPianoRilassato(verticeCurrent, goal, grafo, tempo, maxOrizzonteTemporale)
            if(pathRilassato is not None):
                if(collisionFree(paths, pathRilassato, tempo, goal)):
                    pathRil = combinaPaths(pathRilassato, reconstructPath(init, verticeCurrent, parentDict, tempo, 0))#, contatoreOpen, len(closedList)
                    if(pathRil.calcolaCosto() <= fDict[current]):
                        return pathRil, contatoreOpen, len(closedList)

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
        for mossa in pathRilassato.getMosse():
            if(p.isMossaIllegale(mossa[1].getOrig(), mossa[1].getDst(), mossa[0], goal)):
                return False
    return True

def combinaPaths(pathRilassato, pathReconstruct):
    #aggiunta delle mosse del pathRilassato alla fine del pathReconstruct
    pathReconstruct.invertiMosse() #ordiniamo mosse path parziale costruito con reachgoal classico
    for mossa in pathRilassato.getMosse(): 
        pathReconstruct.addMossa(mossa[0], mossa[1])
    pathReconstruct.setGoal(pathRilassato.getGoal()) #settiamo il goal del path composto
    return pathReconstruct

def setdefault_g(dizionario, chiave, valore_predefinito):
    if chiave not in dizionario:
        dizionario[chiave] = valore_predefinito
    return dizionario[chiave]