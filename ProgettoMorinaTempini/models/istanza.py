import models.grafo as Grafo

class Istanza:
    def __init__(self, griglia, grafo: Grafo):
        self.griglia = griglia
        self.grafo = grafo

    def getGriglia(self):
        return self.griglia
    
    def getGrafo(self):
        return self.grafo