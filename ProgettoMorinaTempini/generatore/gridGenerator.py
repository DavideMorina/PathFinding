import random
from models.griglia import  Griglia

def generaGriglia(nrows, ncols, freeCellRatio, agglomerationFactor):
    griglia = Griglia(nrows, ncols)

    #aggiungi ostacoli
    ratioCelleOcc = 1-freeCellRatio
    numOstacoli = int(nrows * ncols * ratioCelleOcc) #calcoliamo il numero di ostacoli in base a numero celle e ratioOccupiedCells


def aggiungiOstacoli(griglia, numOstacoli, agglomerationFactor):
    if(numOstacoli == 0): return griglia

    numOstacoliAgglomerati=int(numOstacoli * agglomerationFactor)
    creaAgglomerazioni(griglia, numOstacoliAgglomerati) #da chiamare se numOstacoliAgglomerati >=2
    
def creaAgglomerazioni(griglia, numOstacoliAgglomerati):

    agglomerazioni=[] #contiene le varie agglomerazioni con il numero dei rispettivi ostacoli
    while(numOstacoliAgglomerati>=2):
        num=random.randit(2, numOstacoliAgglomerati) #num è il numero di ostacoli in quella agglomerazione
        numOstacoliAgglomerati -= num
        if(numOstacoliAgglomerati<2): num += numOstacoliAgglomerati
        agglomerazioni.append(num)

    
    direzioni=[(1,0), (0,1), (-1,0), (0,-1)]


    for i in range(len(agglomerazioni)): 
               
        primaR = random.randint(0, griglia.getNumRows()-1)
        primaC = random.randint(0, griglia.getNumCols()-1)
        griglia.addOstacolo(primaR, primaC)



    