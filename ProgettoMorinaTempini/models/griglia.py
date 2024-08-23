class Griglia:
    def __init__(self, rows, cols):
        """rows: numero righe
           cols: numero colonne"""
        self.rows = rows
        self.cols = cols

        self.celleOccupate = set() #set contenente le coppie (r,c): celle occupate da ostacolo
        
    def getNumRows(self):
        """Restituisce il numero di righe"""
        return self.rows
    
    def getNumCols(self):
        """Restituisce il numero di colonne"""
        return self.cols
    
    def addOstacolo(self, r, c):
        self.celleOccupate.add((r,c))
