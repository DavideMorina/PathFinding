import random
from models.griglia import  Griglia

def generaGriglia(nrows, ncols, freeCellRatio, agglomerationFactor):
    griglia = Griglia(nrows, ncols)

    #aggiungi ostacoli
    ratioCelleOcc = 1-freeCellRatio
    numOstacoli = int(nrows * ncols * ratioCelleOcc) #calcoliamo il numero di ostacoli in base a numero celle e ratioOccupiedCells

    aggiungiOstacoli(griglia, numOstacoli, agglomerationFactor)
    return griglia


def aggiungiOstacoli(griglia, numOstacoli, agglomerationFactor):
    if(numOstacoli == 0): return griglia

    numOstacoliAgglomerati=int(numOstacoli * agglomerationFactor)

    if(numOstacoliAgglomerati >= 2): 
        creaAgglomerazioni(griglia, numOstacoliAgglomerati)
        numOstacoliRimanenti = numOstacoli-numOstacoliAgglomerati
    else: numOstacoliRimanenti = numOstacoli
    
    while(numOstacoliRimanenti > 0):
        R = random.randint(0, griglia.getNumRows()-1)
        C = random.randint(0, griglia.getNumCols()-1)
        while(griglia.isCellaOccupata(C, R)):
            R = random.randint(0, griglia.getNumRows()-1)
            C = random.randint(0, griglia.getNumCols()-1)
            
        griglia.addOstacolo(C, R)
        numOstacoliRimanenti -= 1


    
def creaAgglomerazioni(griglia, numOstacoliAgglomerati):

    agglomerazioni=[] #contiene le varie agglomerazioni con il numero dei rispettivi ostacoli
    while(numOstacoliAgglomerati>=2):
        num=random.randint(2, numOstacoliAgglomerati) #num è il numero di ostacoli in quella agglomerazione
        numOstacoliAgglomerati -= num
        if(numOstacoliAgglomerati<2): num += numOstacoliAgglomerati
        agglomerazioni.append(num)

    
    print(agglomerazioni)
    direzioni=[(1,0), (0,1), (-1,0), (0,-1)] #direzioni possibili per sviluppare l'aggromerazione

    agglo=[]

    for i in range(len(agglomerazioni)): 
        
   
        primaR = random.randint(0, griglia.getNumRows()-1) #estraggo la prima cella dell'agglo (non deve essere già occupata)
        primaC = random.randint(0, griglia.getNumCols()-1)
        while(griglia.isCellaOccupata(primaC, primaR)):
            primaR = random.randint(0, griglia.getNumRows()-1)
            primaC = random.randint(0, griglia.getNumCols()-1)

        agglo.append((primaC, primaR)) #aggiungo prima cella alla lista di agglomerazione
        griglia.addOstacolo(primaC, primaR) #aggiungo ostacolo in cella
        agglomerazioni[i] -= 1
        while(agglomerazioni[i] > 0): #sviluppo agglomerazione
            
            while True:
                direzione = random.choice(direzioni)
                cella=random.choice(agglo)
                nuovaC = cella[0] + direzione[0]
                nuovaR = cella[1] + direzione[1]
                if (0 <= nuovaR < griglia.getNumRows() and 0 <= nuovaC < griglia.getNumCols() and not griglia.isCellaOccupata(nuovaC, nuovaR)): #controllo che nuova cella esiste e non sia occupata
                    agglo.append((nuovaC, nuovaR))
                    griglia.addOstacolo(nuovaC, nuovaR)
                    agglomerazioni[i] -= 1
                    break
            


    