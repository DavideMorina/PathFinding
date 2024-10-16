from models.path import Path
from models.path import Mossa

def reconstructPath(init,goal,parentDict,t, tRif):
    """ritorna il percorso di costo t tra init e goal"""

    path=Path(init,goal)
    current = goal
    while ( t > tRif ):
        parent = parentDict[(current, t)]
        nodoParent = parent[0]
        path.addMossa(t-1, Mossa(nodoParent, current, path.calcolaPeso(nodoParent, current)))
        
        current = nodoParent
        t -= 1

    path.printPath()
    return path