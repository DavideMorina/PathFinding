import models.istanza
import time 
import os
import pathlib
import tracemalloc

class raccoglitoreInfoTest:
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
        self.lunghezzaPathAgenteRilassato = None
        self.costoAgente = None
        self.costoAgenteRilassato = None
        self.mosseWait = None
        self.mosseWaitRilassato = None
        self.contatoreOpenReachGoal = None
        self.contatoreClosedReachGoal = None
        self.contatoreOpenReachGoalRilassato = None
        self.contatoreClosedReachGoalRilassato = None
        self.time = None
        self.timeGrigliaGrafo = None
        self.timeGridPseudo = None
        self.timeGridReach = None
        self.timeReachGoal = None
        self.timeReachGoalRilassato = None
        self.timeFinale = None
        self.avgMemory = None
        self.peakMemory = None
        self.avgMemoryGrigliaGrafo = None
        self.peakMemoryGrigliaGrafo = None
        self.avgMemoryGridPseudo = None
        self.peakMemoryGridPseudo = None
        self.avgMemoryGridReach = None
        self.peakMemoryGridReach = None
        self.avgMemoryReachGoal = None
        self.peakMemoryReachGoal = None
        self.avgMemoryReachGoalRilassato = None
        self.peakMemoryReachGoalRilassato = None

    """ A seguire una serie di metodi necessari a tenere traccia del tempo impiegata e 
    della memoria utilizzata per svolgere i vari compiti"""

    def iniziaMonitoraggioGrigliaGrafo(self):
        self.timeGrigliaGrafo=time.time()
        tracemalloc.start()
        
    def iniziaMonitoraggioGridPseudo(self):
        self.timeGridPseudo=time.time()
        tracemalloc.start()

    def iniziaMonitoraggioGridReach(self):
        self.timeGridReach=time.time()
        tracemalloc.start()

    def iniziaMonitoraggioReachGoal(self):
        self.timeReachGoal=time.time()
        tracemalloc.start()

    def iniziaMonitoraggioReachGoalRilassato(self):
        self.timeReachGoalRilassato=time.time()
        tracemalloc.start()

    def terminaMonitoraggioGrigliaGrafo(self):
        self.timeGrigliaGrafo = time.time() - self.timeGrigliaGrafo
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        self.avgMemoryGrigliaGrafo = current / 1000000 #portiamo in MB
        self.peakMemoryGrigliaGrafo = peak / 1000000   #portiamo in MB

    def terminaMonitoraggioGridReach(self):
        self.timeGridReach = time.time() - self.timeGridReach
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        self.avgMemoryGridReach = current / 1000000 #portiamo in MB
        self.peakMemoryGridReach = peak / 1000000   #portiamo in MB

    def terminaMonitoraggioGridPseudo(self):
        self.timeGridPseudo = time.time() - self.timeGridPseudo
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        self.avgMemoryGridPseudo = current / 1000000 #portiamo in MB
        self.peakMemoryGridPseudo = peak / 1000000   #portiamo in MB
        
    def terminaMonitoraggioReachGoal(self):
        self.timeReachGoal = time.time() - self.timeReachGoal
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        self.avgMemoryReachGoal = current / 1000000 #portiamo in MB
        self.peakMemoryReachGoal = peak / 1000000   #portiamo in MB

    def terminaMonitoraggioReachGoalRilassato(self):
        self.timeReachGoalRilassato = time.time() - self.timeReachGoalRilassato
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        self.avgMemoryReachGoalRilassato = current / 1000000 #portiamo in MB
        self.peakMemoryReachGoalRilassato = peak / 1000000   #portiamo in MB

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
        self.contatoreOpenReachGoal = contatoreOpen

    def setContatoreClosed(self, contatoreClosed):
        self.contatoreClosedReachGoal = contatoreClosed

    def setLunghezzaPathAgenteRilassato(self, lunghezzaPathAgenteRilassato):
        self.lunghezzaPathAgenteRilassato = lunghezzaPathAgenteRilassato

    def setCostoAgenteRilassato(self, costoAgenteRilassato):
        self.costoAgenteRilassato = costoAgenteRilassato

    def setMosseWaitRilassato(self, mosseWaitRilassato):
        self.mosseWaitRilassato = mosseWaitRilassato

    def setContatoreOpenRilassato(self, contatoreOpenRilassato):
        self.contatoreOpenReachGoalRilassato = contatoreOpenRilassato

    def setContatoreClosedRilassato(self, contatoreClosedRilassato):
        self.contatoreClosedReachGoalRilassato = contatoreClosedRilassato
        
    def setTime(self):
        self.time = time.time()
        
    def setTimeFinale(self):
        self.timeFinale = time.time() - self.time

    def computaWait(self, pathAgente):
        """ Metodo necessario per il calcolo delle mosse wait """
        if not pathAgente:
            return None
        count=0
        for _,mossa in pathAgente.getMosse():
            if mossa.getOrig() == mossa.getDst():
                count +=1
        self.setMosseWait(count)

    def computaWaitRilassato(self, pathAgenteRilassato):
        """Metodo per calcolare il numero di mosse wait eseguite in un path
        
        Parametri: path
        Restituisce: nessuno
        
        setta l'attributo mosseWait con il numero di mosse wait eseguite dal path dell'entry agent"""
        if not pathAgenteRilassato:
            return None
        count=0
        for _,mossa in pathAgenteRilassato.getMosse():
            if mossa.getOrig() == mossa.getDst():
                count +=1
        self.setMosseWaitRilassato(count)

    def setValori(self, istanza, freeCellRatio, fattoreAgglomerazione, nagents, usatoReachGoal, usatoRilassato, limiteLunghezzaPathsEsistenti, lunghezzePathsEsistenti, maxOrizzonteTemporale, initAgente, goalAgente, lunghezzaPathAgente, lunghezzaPathAgenteRilassato, costoPathAgenteReachGoal, costoPathAgenteReachGoalRilassato, pathAgenteReachGoal, pathAgenteReachGoalRilassato, contatoreOpenReachGoal, contatoreOpenReachGoalRilassato, contatoreClosedReachGoal, contatoreClosedReachGoalRilassato):
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
        self.setLunghezzaPathAgenteRilassato(lunghezzaPathAgenteRilassato)
        self.setCostoAgente(costoPathAgenteReachGoal)
        self.setCostoAgenteRilassato(costoPathAgenteReachGoalRilassato)
        self.computaWait(pathAgenteReachGoal)
        self.computaWaitRilassato(pathAgenteReachGoalRilassato)
        self.setContatoreOpen(contatoreOpenReachGoal)
        self.setContatoreOpenRilassato(contatoreOpenReachGoalRilassato)
        self.setContatoreClosed(contatoreClosedReachGoal)
        self.setContatoreClosedRilassato(contatoreClosedReachGoalRilassato)
        

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

        directory = os.path.join(pathlib.Path(__file__).parent.resolve(), "file_output_test")
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
            file.write("Usato piano rilassato per generazione istanza\n")
        else:
            file.write("Non usato piano rilassato per generazione istanza\n")
            
        file.write("Lunghezza massima dei percorsi degli agenti preesistenti: "+str(self.limiteLunghezzaPathsEsistenti)+"\n") #lunghezza max path agenti se non si usa rachgoal
        file.write("Lunghezza dei percorsi degli agenti preesistenti: \n") 
        for i,l in enumerate(self.lunghezzePathsEsistenti):
            file.write("\tPath "+str(i+1)+": "+str(l)+"\n")
        
        #info sull'n+1 agente
        file.write("Valore max orizzonte temporale: "+str(self.maxOrizzonteTemporale)+"\n")
        file.write("Init n+1-esimo agente: "+str(self.initAgente)+"\n")   
        file.write("Goal n+1-esimo agente: "+str(self.goalAgente)+"\n")  
        file.write("----------------------------------------------------------------\n")
        file.write("Risoluzione con ReachGoal normale:\n")
        file.write("Lunghezza del percorso dell' n+1-esimo agente: "+str(self.lunghezzaPathAgente)+"\n") 
        file.write("Costo del percorso dell' n+1-esimo agente: "+str(self.costoAgente)+"\n")
        file.write("Numero di mosse wait: "+str(self.mosseWait)+"\n")
        file.write("Numero stati espansi in lista open: "+str(self.contatoreOpenReachGoal)+"\n")
        file.write("Numero stati espansi in lista closed: "+str(self.contatoreClosedReachGoal)+"\n")
    

        file.write("----------------------------------------------------------------\n")
        file.write("Risoluzione con ReachGoal rilassato:\n") 
        file.write("Lunghezza del percorso dell' n+1-esimo agente: "+str(self.lunghezzaPathAgenteRilassato)+"\n") 
        file.write("Costo del percorso dell' n+1-esimo agente: "+str(self.costoAgenteRilassato)+"\n")
        file.write("Numero di mosse wait: "+str(self.mosseWaitRilassato)+"\n")
        file.write("Numero stati espansi in lista open: "+str(self.contatoreOpenReachGoalRilassato)+"\n")
        file.write("Numero stati espansi in lista closed: "+str(self.contatoreClosedReachGoalRilassato)+"\n")


        #info generali esecuzione
        file.write("----------------------------------------------------------------\n")
        file.write("Generazione griglia e grafo: \n")
        file.write("Tempo di esecuzione: "+str(self.timeGrigliaGrafo)+" secondi\n")
        file.write("Memoria utilizzata: "+str(self.avgMemoryGrigliaGrafo)+" MB \n")
        file.write("Picco di memoria: "+str(self.peakMemoryGrigliaGrafo)+" MB \n")

        file.write("----------------------------------------------------------------\n")
        file.write("Generazione istanza pseudo casuale: \n")
        file.write("Tempo di esecuzione: "+str(self.timeGridPseudo)+" secondi\n")
        file.write("Memoria utilizzata: "+str(self.avgMemoryGridPseudo)+" MB \n")
        file.write("Picco di memoria: "+str(self.peakMemoryGridPseudo)+" MB \n")

        file.write("----------------------------------------------------------------\n")
        file.write("Generazione istanza con ReachGoal: \n")
        file.write("Tempo di esecuzione: "+str(self.timeGridReach)+" secondi\n")
        file.write("Memoria utilizzata: "+str(self.avgMemoryGridReach)+" MB \n")
        file.write("Picco di memoria: "+str(self.peakMemoryGridReach)+" MB \n")

        file.write("----------------------------------------------------------------\n")
        file.write("Risoluzione istanza con ReachGoal normale: \n")
        file.write("Tempo di esecuzione: "+str(self.timeReachGoal)+" secondi\n")
        file.write("Memoria utilizzata: "+str(self.avgMemoryReachGoal)+" MB \n")
        file.write("Picco di memoria: "+str(self.peakMemoryReachGoal)+" MB \n")

        file.write("----------------------------------------------------------------\n")
        file.write("Risoluzione istanza con ReachGoal rilassato: \n")
        file.write("Tempo di esecuzione: "+str(self.timeReachGoalRilassato)+" secondi\n")
        file.write("Memoria utilizzata: "+str(self.avgMemoryReachGoalRilassato)+" MB \n")
        file.write("Picco di memoria: "+str(self.peakMemoryReachGoalRilassato)+" MB \n")

        file.close()    #chiudere il file!