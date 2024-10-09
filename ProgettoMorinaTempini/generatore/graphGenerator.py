import math
from models.grafo import Grafo

def generaGrafoDaGriglia(griglia):

    mosseCardinali=[(0,0), (1,0), (-1,0), (0,1), (0,-1)]
    mosseDiagonali=[(1,1), (1, -1), (-1,1), (-1,-1)]

    righe, colonne = griglia.getNumRows(), griglia.getNumCols()

    grafo=Grafo()

    for r in range(righe):
        for c in range(colonne):
            if not griglia.isCellaOccupata(c, r):
                for mossa in mosseCardinali:
                    newc = c + mossa[0]
                    newr = r + mossa[1]
                    if 0 <= newr < righe and 0 <= newc < colonne and not griglia.isCellaOccupata(newc, newr):
                        grafo.aggiungi_arco((c,r),(newc,newr),1)
                        
                for mossa in mosseDiagonali:
                    newc = c + mossa[0]
                    newr = r + mossa[1]
                    if 0 <= newr < righe and 0 <= newc < colonne and not griglia.isCellaOccupata(newc, newr):
                        grafo.aggiungi_arco((c,r),(newc,newr),math.sqrt(2))
                        
                
    return grafo