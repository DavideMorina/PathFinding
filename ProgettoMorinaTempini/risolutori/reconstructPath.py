from models.path import Path
from models.path import Mossa

def reconstructPath(init,goal,parentDict,t, tRif):
    """
    Metodo per la ricostruzione del percorso
    Parametri: init, goal, parentDict, tempo t, tempo di riferimento tRif
    Restituisce: path
    
    Sulla base dei tempi e della lista dei genitori, ricostruisce il percorso in tutte le sue mosse"""

    path=Path(init,goal)
    current = goal
    while ( t > tRif ):
        parent = parentDict[(current, t)]
        nodoParent = parent[0]
        path.addMossa(t-1, Mossa(nodoParent, current, path.calcolaPeso(nodoParent, current)))
        
        current = nodoParent
        t -= 1

    return path
