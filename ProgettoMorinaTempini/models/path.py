import math

class Mossa:
    def __init__(self, orig, dst, peso):
        self.orig = orig
        self.dst = dst
        self.peso = peso

    def __str__(self):
        return "(" + str(self.orig) + "->" + str(self.dst) + "," + str(self.peso) + ")"

    def getOrig(self):
        return self.orig
    
    def getDst(self):
        return self.dst
    
    def getPeso(self):
        return self.peso
    
    def printMossa(self):
        print(f"Mossa: ({self.orig[0]}, {self.orig[1]}) -> ({self.dst[0]}, {self.dst[1]}), "+{self.pes})


class Path:
    def __init__(self, init, goal):
        self.mosse = {} #hash: chiave=tempo t, valore=Mossa(orig, dest, peso)
        self.init = init
        self.goal = goal
        self.lunghezza = 0

    def getInit(self):
        return self.init
    
    def getGoal(self):
        return self.goal
    
    def getLunghezza(self):
        return self.lunghezza
    
    def setGoal(self, goal):
        self.goal = goal

    def setInit(self, init):
        self.init = init
    
    def addMossa(self, tempo, mossa):
        self.mosse[tempo] = mossa
        self.lunghezza += 1

    def getMossa(self, tempo):
        return self.mosse.get(tempo)
    
    def getMosse(self):
        return self.mosse.items()

    def invertiMosse(self):
        self.mosse = {k: self.mosse[k] for k in reversed(self.mosse)}

    def esisteMossaAlTempoT(self, tempo):
        return tempo in self.mosse
    
    def checkCollisioneDiagonale(self, orig, dst, tempo):
        """Metodo che controlla l'eventuale scambio in diagonale"""
        
        #coordinate della mossa del path p nella griglia
        orig_p_c = self.getMossa(tempo).getOrig()[0]
        orig_p_r = self.getMossa(tempo).getOrig()[1]
        dst_p_c = self.getMossa(tempo).getDst()[0]
        dst_p_r = self.getMossa(tempo).getDst()[1]

        #stessa colonna
        if(orig_p_c == orig[0]):
            if(orig_p_r == orig[1]-1): #orig è sopra orig_p
                if (dst_p_c == dst[0] and dst_p_r == dst[1]+1): return True

            elif(orig_p_r == orig[1]+1): #orig è sotto orig_p
                if (dst_p_c == dst[0] and dst_p_r == dst[1]-1): return True

        #stessa riga
        elif( orig_p_r == orig[1] and (() or ()) ):
            if(orig_p_c == orig[0]-1): #orig è a destra di orig_p
                if (dst_p_r == dst[1] and dst_p_c == dst[0]+1): return True
            
            elif(orig_p_c == orig[0]+1): #orig è a sinistra di orig_p
                if (dst_p_r == dst[1] and dst_p_c == dst[0]-1): return True

        return False
    
    def passeraSulGoal(self, tempo, goal):
        """Metodo per il controllo della collisione dovuta al fermarsi sul goal troppo presto"""
        for chiaveMossa in self.mosse: #chiaveMossa è anche il tempo associato a quella mossa
            t=chiaveMossa
            mossa = self.getMossa(chiaveMossa)
            if(mossa.getDst() == goal and t>tempo):
                return True
        return False
     
    def isMossaIllegale(self, orig, dst, tempo, goal=None):
        """Metodo per il controllo di tutte le eventuali collisioni
        Parametri: cella origine, cella destinazione, tempo della mossa, eventuale goal
        Restituisce: True se mossa illegale, Fale se legale
        
        Si controllano i vari casi di collisione"""
        #caso 1: allo stesso tempo dest uguale
        if(self.esisteMossaAlTempoT(tempo) and dst == self.getMossa(tempo).getDst()):
            return True
        #caso 2: si scambiano
        elif(self.esisteMossaAlTempoT(tempo) and orig == self.getMossa(tempo).getDst() and dst == self.getMossa(tempo).getOrig()):
            return True
        #caso 3: altro agente ha finito (ed è al goal)
        elif(not self.esisteMossaAlTempoT(tempo) and dst == self.getGoal()):
            return True
        #caso 4: raggiunge e si ferma al goal, ma in quella casella dovrà passare il percorso self in un tempo futuro
        elif(goal!=None and dst == goal and self.passeraSulGoal(tempo, goal)):
            return True
        #caso 5: scambio in diagonale
        elif(self.esisteMossaAlTempoT(tempo)):
            return self.checkCollisioneDiagonale(orig, dst, tempo)
        #nessuna delle precedenti si è verificata --> mossa legale
        return False;     

    def calcolaCosto(self):
        """Metodo per calcolare il costo del percorso"""
        costo=0
        for chiaveMossa in self.mosse:
            mossa = self.getMossa(chiaveMossa)
            costo += mossa.peso
        return costo

    @staticmethod
    def rimuoviMosseIllegali(mossedisponibili, tempo, attuale, paths):
        """Metodo per la rimozione delle mosse illegali
        Parametri: mosse disponibili, tempo, cella attuale, paths
        Restituisce: lista mossedisponibili filtrata"""
        for arco in mossedisponibili :
            for p in paths:
                if p.isMossaIllegale(attuale, arco.dest, tempo):
                    mossedisponibili.remove(arco)
                    break

        return mossedisponibili  

    @staticmethod
    def rimuoviArriviIllegali(mossedisponibili, tempo, paths):
        """Metodo per la rimozione degli arrivi illegali
        Parametri: mosse disponibili, tempo, paths
        Restituisce: lista mossedisponibili filtrata"""
        for arco in mossedisponibili :
            for p in paths:
                if p.passeraSulGoal(tempo, arco.dest):
                    mossedisponibili.remove(arco)
                    break

        return mossedisponibili


    @staticmethod
    def calcolaPeso(init, dest):
        """Metodo per calcolare il peso di un arco"""
        mosseCardinali = Path.getMosseCardinali() 
        mosseDiagonali = Path.getMosseDiagonali() 
        
        if (dest[0] - init[0], dest[1] - init[1]) in mosseCardinali:
            return 1
        elif (dest[0] - init[0], dest[1] - init[1]) in mosseDiagonali:
            return math.sqrt(2)
    
    @staticmethod
    def getMosseCardinali():
        return [(0,0), (-1,0), (1,0), (0,-1), (0,1)]
    
    @staticmethod
    def getMosseDiagonali():
        return [(1,1), (-1,1), (-1,-1), (1,-1)]

    def printPath(self):
        """Metodo per la stampa del percorso"""
        # print start node, end goal node e mosse per collegarli
        print("\n--------------------")
        print("Start node: ", self.getInit())
        print("Goal node: ", self.getGoal())
        print("Path: ")
        for mossa in self.mosse:
            print(self.getMossa(mossa), mossa)


