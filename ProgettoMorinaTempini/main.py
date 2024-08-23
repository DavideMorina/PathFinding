import generatore.istanceGenerator as istanceGenerator

def main():
    rows=10
    col=10
    fattore_agglomerazione=0.2
    freeCellRatio=0.7

    istanza = istanceGenerator.generaIstanza(rows, col, fattore_agglomerazione, freeCellRatio)
    
if __name__ == "__main__":
    main()