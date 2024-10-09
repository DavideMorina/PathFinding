import models.istanza
import time 
import os
import pathlib
import tracemalloc

class raccoglitoreInfo:
    def __init__(self):
        self.istanza = None
        self.freeCellRatio = None
        self.fattoreAgglomerazione = None
        self.nagents = None
        self.limiteLunghezzaPathsEsistenti = None
        self.lunghezzePathsEsistenti = None
        self.usatoReachGoal = None
        self.usatoRilassato = None
        self.maxOrizzonteTemporale = None
        self.initAgente = None
        self.goalAgente = None
        self.lunghezzaPathAgente = None #n+1-esimo agente
        self.costoAgente = None
        self.mosseWait = None
        self.contatoreOpen = None
        self.contatoreClosed = None
        self.time = None
        self.timeFinale = None
        self.avgMemory = None
        self.peakMemory = None

    def iniziaMonitoraggio(self):
        self.time=time.time()
        tracemalloc.start()

    def terminaMonitoraggio(self):
        self.setTimeFinale()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        self.avgMemory = current / 1000000 #portiamo in MB
        self.peakMemory = peak / 1000000   #portiamo in MB
        #return avgMemory, peakMemory
    
        #print(f"Current memory usage is {current / 10**6}MB; Peak memory usage is {peak / 10**6}MB")
        #print(f"Tempo di esecuzione: {self.timeFinale - self.time} secondi")

    def getIstanza(self):
        return self.istanza

    def getFreeCellRatio(self):
        return self.freeCellRatio
    
    def getFattoreAglomerazione(self):
        return self.fattoreAgglomerazione
    

    def setIstanza(self, istanza):
        self.istanza = istanza

    def setFreeCellRatio(self, freeCellRatio):
        self.freeCellRatio = freeCellRatio

    def setFattoreAgglomerazione(self, fattoreAgglomerazione):
        self.fattoreAgglomerazione = fattoreAgglomerazione

    def setNAgents(self, nagents):
        self.nagents = nagents

    def setLimiteLunghezzaPathsEsistenti(self, limiteLunghezzaPathsEsistenti):
        self.limiteLunghezzaPathsEsistenti = limiteLunghezzaPathsEsistenti
    
    def setLunghezzePathsEsistenti(self, lunghezzePathsEsistenti):
        self.lunghezzePathsEsistenti = lunghezzePathsEsistenti

    def setUsatoReachGoal(self, usatoReachGoal):
        self.usatoReachGoal = usatoReachGoal

    def setUsatoRilassato(self, usatoRilassato):
        self.usatoRilassato = usatoRilassato

    def setMaxOrizzonteTemporale(self, maxOrizzonteTemporale):
        self.maxOrizzonteTemporale = maxOrizzonteTemporale

    def setInitAgente(self, initAgente):
        self.initAgente = initAgente

    def setGoalAgente(self, goalAgente):
        self.goalAgente = goalAgente
        
    def setLunghezzaPathAgente(self, lunghezzaPathAgente):
        self.lunghezzaPathAgente = lunghezzaPathAgente

    def setCostoAgente(self, costoAgente):
        self.costoAgente = costoAgente

    def setMosseWait(self, mosseWait):
        self.mosseWait = mosseWait

    def setContatoreOpen(self, contatoreOpen):
        self.contatoreOpen = contatoreOpen

    def setContatoreClosed(self, contatoreClosed):
        self.contatoreClosed = contatoreClosed

    def setTime(self):
        self.time = time.time()
        
    def setTimeFinale(self):
        self.timeFinale = time.time() - self.time

    def computaWait(self, pathAgente):
        if not pathAgente:
            return None
        count=0
        for _,mossa in pathAgente.getMosse():
            if mossa.getOrig() == mossa.getDst():
                count +=1
        self.setMosseWait(count)

    def setValori(self, istanza, freeCellRatio, fattoreAgglomerazione, nagents, usatoReachGoal, usatoRilassato, limiteLunghezzaPathsEsistenti, lunghezzePathsEsistenti, maxOrizzonteTemporale, initAgente, goalAgente, lunghezzaPathAgente, costoAgente, pathAgente, contatoreOpen, contatoreClosed):
        self.setIstanza(istanza)
        self.setFreeCellRatio(freeCellRatio)
        self.setFattoreAgglomerazione(fattoreAgglomerazione)
        self.setNAgents(nagents)
        self.setUsatoReachGoal(usatoReachGoal)
        self.setUsatoRilassato(usatoRilassato)
        self.setLimiteLunghezzaPathsEsistenti(limiteLunghezzaPathsEsistenti)
        self.setLunghezzePathsEsistenti(lunghezzePathsEsistenti)
        self.setMaxOrizzonteTemporale(maxOrizzonteTemporale)
        self.setInitAgente(initAgente)
        self.setGoalAgente(goalAgente)
        self.setLunghezzaPathAgente(lunghezzaPathAgente)
        self.setCostoAgente(costoAgente)
        self.computaWait(pathAgente)
        self.setContatoreOpen(contatoreOpen)
        self.setContatoreClosed(contatoreClosed)

    def printInfo(self):
        print("Numero di righe: ", self.istanza.getGriglia().getNumRows())
        print("Numero di colonne: ", self.istanza.getGriglia().getNumCols())
        print("Rapporto di celle libere: ", self.freeCellRatio)
        print("Fattore di agglomerazione: ", self.fattoreAgglomerazione)
        print("Numero di agenti: ", self.nagents)
        if(self.usatoReachGoal):
            print("Usato ReachGoal")
        else:
            print("Usata generazione pseudo-casuale")
        if(self.usatoRilassato):
            print("Usato piano rilassato")
        else:
            print("Non usato piano rilassato")
        print("Lunghezza massima dei percorsi degli agenti preesistenti: ", self.limiteLunghezzaPathsEsistenti)
        print("Lunghezza dei percorsi degli agenti preesistenti: \n")
        for i,l in enumerate(self.lunghezzePathsEsistenti):
            print("\tPath "+str(i+1)+": "+str(l))
        print("Max Orizzonte Temporale: ", self.maxOrizzonteTemporale)
        print("Init Agente: ", self.initAgente)
        print("Goal Agente: ", self.goalAgente)
        print("Lunghezza del percorso dell' n+1-esimo agente : ", self.lunghezzaPathAgente)
        print("Costo agente: ", self.costoAgente)
        print("Numero di mosse wait: ", self.mosseWait)
        print("Numero stati espansi in lista open: ", self.contatoreOpen)
        print("Numero stati espansi in lista closed: ", self.contatoreClosed)
        print("Tempo di esecuzione: ", self.timeFinale)
        print("Memoria utilizzata: ", self.avgMemory, "MB")
        print("Picco di memoria: ", self.peakMemory, "MB")
        

    def scriviInfoSuFile(self):
        """
        Questa funzione scrive informazioni sull'istanza e sull'n+1-esimo agente in un file di testo.
        Parametri: Nessuno

        Restituisce: Nessuno

        La funzione crea una directory denominata 'file_output' se non esiste, quindi scrive le seguenti informazioni in un file di testo:
        - La data e l'ora di creazione del file
        - Informazioni sull'istanza (numero di righe, colonne, rapporto celle libere, fattore di aggregazione, numero di agenti, utilizzo di reachgoal, lunghezza massima dei percorsi esistenti)
        - Informazioni sull'n+1-esimo agente (orizzonte temporale massimo, posizione iniziale, posizione obiettivo, lunghezza del percorso, costo del percorso, numero di nodi espansi in lista aperta, numero di nodi espansi in lista chiusa)
        - Informazioni generali sull'esecuzione (tempo di esecuzione)
        """

        directory = os.path.join(pathlib.Path(__file__).parent.resolve(), "file_output")
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = os.path.join(directory, "informazioni_istanza_" + str(time.time()) + ".txt")
        file = open(filename, "w")

        file.write("Generato il: "+str(time.ctime())+"\n")
        #info sull'istanza
        file.write("Numero di righe: "+str(self.istanza.getGriglia().getNumRows())+"\n")
        file.write("Numero di colonne: "+ str(self.istanza.getGriglia().getNumCols())+"\n")
        file.write("Rapporto di celle libere: "+ str(self.freeCellRatio)+"\n")
        file.write("Fattore di agglomerazione: "+ str(self.fattoreAgglomerazione)+"\n")
        file.write("Numero di agenti: "+str(self.nagents)+"\n")
        if(self.usatoReachGoal):
            file.write("Usato ReachGoal \n")
        else:
            file.write("Usata generazione pseudo-casuale \n")
        if(self.usatoRilassato):
            file.write("Usato piano rilassato \n")
        else:
            file.write("Non usato piano rilassato \n")
            
        file.write("Lunghezza massima dei percorsi degli agenti preesistenti: "+str(self.limiteLunghezzaPathsEsistenti)+"\n") #lunghezza max path agenti se non si usa rachgoal
        file.write("Lunghezza dei percorsi degli agenti preesistenti: \n") 
        for i,l in enumerate(self.lunghezzePathsEsistenti):
            file.write("\tPath "+str(i+1)+": "+str(l)+"\n")
        
        #info sull'n+1 agente
        file.write("Valore max orizzonte temporale: "+str(self.maxOrizzonteTemporale)+"\n")
        file.write("Init n+1-esimo agente: "+str(self.initAgente)+"\n")   
        file.write("Goal n+1-esimo agente: "+str(self.goalAgente)+"\n")  
        file.write("Lunghezza del percorso dell' n+1-esimo agente: "+str(self.lunghezzaPathAgente)+"\n") 
        file.write("Costo del percorso dell' n+1-esimo agente: "+str(self.costoAgente)+"\n")
        file.write("Numero di mosse wait: "+str(self.mosseWait)+"\n")
        file.write("Numero stati espansi in lista open: "+str(self.contatoreOpen)+"\n")
        file.write("Numero stati espansi in lista closed: "+str(self.contatoreClosed)+"\n")

        #info generali esecuzione
        file.write("Tempo di esecuzione: "+str(self.timeFinale)+" secondi\n")
        file.write("Memoria utilizzata: "+str(self.avgMemory)+" MB \n")
        file.write("Picco di memoria: "+str(self.peakMemory)+" MB \n")

        file.close()    #chiudere il file!




   