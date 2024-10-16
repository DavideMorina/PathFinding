class Griglia:
    def __init__(self, rows, cols):
        """rows: numero righe
           cols: numero colonne"""
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
        return (c,r) in self.celleOccupate
    
    def getNumCelleLibere(self):
        return (self.rows*self.cols) - len(self.celleOccupate)
