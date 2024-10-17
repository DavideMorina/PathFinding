from .euristica import calcolaEuristica
from .reconstructPath import reconstructPath
from models.path import Path
from models.path import Mossa
"""def calcolaPianoRilassato(vertice, goal, grafo, tempo, maxOrizzonteTemporale):
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
	
    return path"""

def calcolaPianoRilassato(init, goal, grafo, tempoStart, maxOrizzonteTemporale):
    """calcola un percorso tra init e goal: versione di reachgoal che non tiene conto degli altri paths"""

    #stato si riferisce a coppia (vertice,tempo)
    closedList=[] #lista degli stati già espansi
    openList=[(init, tempoStart)] #lista di stati da espandere
    contatoreOpen=0

    parentDict = {} #chiave: coppia (vertice,tempo), valore: coppia (vertice tempo) genitore
    gDict = {} #chiave: coppia (vertice,tempo), valore: valore di g(vertice,tempo)
    
    gDict[(init, tempoStart)] = 0
    euristica = calcolaEuristica(grafo, goal) #hash di euristiche, chiave: coppia (vertice,goal), valore: h(vertice,goal)

    fDict = {} #chiave: coppia(vertice,tempo), valore: g(vertice,goal)+h(vertice,goal)
    fDict[(init, tempoStart)] = euristica[(init, goal)]   

    while (len(openList)>0):
        #stato con f minore
        current = min(openList, key=lambda x: fDict[x]) #current è l'elemento della openList con il rispettivo valore di f minore
        tempo = current[1]
        verticeCurrent = current[0]
        openList.remove(current)
        closedList.append(current)
        if (verticeCurrent == goal):
            print("££££££££££££")
            return reconstructPath(init,goal,parentDict,tempo,tempoStart)#, contatoreOpen, len(closedList)

        if (tempo < maxOrizzonteTemporale):
            for arco in grafo.getVicini(verticeCurrent):
                nodo=arco.dest
                peso=arco.peso
                nextTempo = tempo + 1
                if((nodo,nextTempo) not in closedList):
                    setdefault_g(gDict, (nodo, nextTempo), float('inf'))
                    if(gDict[(verticeCurrent, tempo)] + peso < gDict[(nodo, nextTempo)]):
                        parentDict[(nodo, nextTempo)] = (verticeCurrent, tempo)
                        gDict[(nodo, nextTempo)] = gDict[(verticeCurrent, tempo)] + peso
                        fDict[(nodo, nextTempo)] = gDict[(nodo, nextTempo)] + euristica[(nodo, goal)]
                    if((nodo, nextTempo) not in openList):
                        openList.append((nodo, nextTempo))  
                        contatoreOpen+=1   

    return None#, None, None


def setdefault_g(dizionario, chiave, valore_predefinito):
    if chiave not in dizionario:
        dizionario[chiave] = valore_predefinito
    return dizionario[chiave]