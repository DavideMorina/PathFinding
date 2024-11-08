class Griglia:
    def __init__(self, rows, cols):
        """rows: numero righe
           cols: numero colonne"""
        #CELLA: coppia (colonna, riga) -> colonna = x, riga = y
        self.rows = rows
        self.cols = cols

        self.celleOccupate = set() #set contenente le coppie (c,r): celle occupate da ostacolo
        
    def getNumRows(self):
        """Restituisce il numero di righe"""
        return self.rows
    
    def getNumCols(self):
        """Restituisce il numero di colonne"""
        return self.cols
    
    def addOstacolo(self, c, r):
        self.celleOccupate.add((c,r))

    def isCellaOccupata(self, c, r):
        """Restituisce True se la cella (c,r) è occupata da un ostacolo, False altrimenti"""
        return (c,r) in self.celleOccupate
    
    def getNumCelleLibere(self):
        """Restituisce il numero di celle libere nella griglia"""
        return (self.rows*self.cols) - len(self.celleOccupate)
