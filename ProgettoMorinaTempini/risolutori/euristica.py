import math

def calcolaEuristica(grafo, goal):
    """
    Metodo per il calcolo dell'euristica
    Parametri: grafo, goal
    Restituisce: euristica
    
    Ritorna un dizionario con tutti i valori di h (distanza diagonale)
    CHIAVE: coppia (vertice,goal)
    VALORE: valore euristica"""

    h=dict()

    #usiamo la distanza diagonale come euristica
    for vertice in grafo.getNodi():
        #if vertice != goal:
            dx = abs(vertice[0] - goal[0])
            dy = abs(vertice[1] - goal[1])
            h[(vertice, goal)] = (dx + dy) + (math.sqrt(2)-2) * min(dx,dy)

    return h