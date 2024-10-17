from models.path import Path
from models.path import Mossa
from risolutori.reachGoal import reachGoal
import random

def generaPaths(inits, goalinit, nagents, limiteLunghezzaPathsEsistenti, grafo):

    """Per ogni agente, a partire dalla sua cella iniziale, costruiamo randomicamente il suo percorso fino al suo goal, anch'esso random.
    La lunghezza del percorso è anchessa radomica, ma contenuta dal parametro limiteLunghezzaPathsEsistenti. I goal devono essere diversi
    tra loro."""

    paths = []


    for i in range(nagents):
        limitePath = random.randint(1, limiteLunghezzaPathsEsistenti) #lunghezze diverse per agenti diversi
        
        init=inits.pop()
        path=Path(init, None)

        tempo=0
        attuale=init

        while(tempo<limitePath):
            mossedisponibili = grafo.getVicini(attuale) #lista di archi: (dest, peso)
            mossedisponibili = Path.rimuoviMosseIllegali(mossedisponibili, tempo, attuale, paths)
            
            if len(mossedisponibili)==0:
                print("Il path per l'agente ("+ str(i+1) +") non aveva mosse diponibili")
                return None
            
            if(tempo==limitePath-1): #sono all'ultima mossa
                for arco in mossedisponibili:
                    #print(arco.dest)
                    mossedisponibili = Path.rimuoviArriviIllegali(mossedisponibili, tempo, paths)
                    if arco.dest in list(goalinit.keys()): #se vado sul goal dell'n+1
                        mossedisponibili.remove(arco)
                        break    
                    

            arco=random.choice(mossedisponibili)

            #controllo per numero volte che si passa sui gol ????
            
            path.addMossa(tempo, Mossa(attuale, arco.dest, arco.peso))
            attuale=arco.dest
            tempo+=1
        
        path.setGoal(attuale)
        paths.append(path)
        #robe lunghezza path ??
            
    return paths

def generaPathsReachGoal(goalsinits, nagents, maxOrizzonteTemporale, grafo, usaRilassato):
    
    paths=[]

    for i in range(nagents):
        goal, init = goalsinits.popitem()

        path, _, _=reachGoal(grafo, paths, init, goal, maxOrizzonteTemporale, usaRilassato)

        if not path:
            print("Il path per l'agente ("+ str(i+1) +") non aveva mosse diponibili")
            return None
        
        ###roba del passare sui goal
        paths.append(path)

    return paths