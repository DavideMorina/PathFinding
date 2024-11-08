from collections import defaultdict

class Arco:
    def __init__(self, d, w):
        self.dest = d
        self.peso = w

    
class Grafo:
    def __init__(self):
        """Hashmap chiave valore: la chiave è il vertice, il valore è una coppia (dest, w) 
        dove dest è il nodo di destinazione, w è il peso associato a tale spostamento. (dest, w) corrisponde quindi ad un arco, 
        che infatti è caratterizzato dalle stesse grandezze"""
        self.vicini=defaultdict(list) #list per dire che il value è una list

    def aggiungi_arco(self, orig, dest, peso):
        """Aggiunge un arco tra orig e dest con il peso specificato"""
        self.vicini[orig].append(Arco(dest, peso))

    def contieneVertice(self, vertice):
        return vertice in self.vicini

    def getNodi(self):
        return self.vicini.keys()

    def getVicini(self, vertice):
        """"
        Ritorna una lista di vicini che sono adiacenti ad un dato vertice
		"""
        return self.vicini[vertice]
    
    def printGrafo(self):
        """Metodo per la stampa del percorso"""
        print("GRAFO")
        for orig, vicini in self.vicini.items():
            print(f"{orig} ->", end=" ")
            for vicino in vicini:
                print(f"[{vicino.dest}, {vicino.peso}];", end=" ")
            print()