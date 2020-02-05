Il seguente progetto utilizza un server in Python costruito con il modulo flask.
A partire dalla pagina principale index.html è possibile selezionare un file contenente un grafo in formato json o graphml [nodes: id, type, name| links: source, target], impostando una serie di parametri a seconda dell'estetica che si preferisce valorizzare maggiormente (distanza tra nodi, lunghezza degli archi, numero di incroci), seguendo le linee guida dell'algoritmo proposto da Davidson e Harel nel 1996.
Premendo il bottone "genera il grafo" viene mandata una richiesta Ajax al server, che elabora il grafo generando le posizioni per i nodi.
La risposta restituita dal server viene infine visualizzata utilizzando d3.js
A partire dal grafo visualizzato è possibile spostarlo trascinandolo con il mouse, effettuare lo zoom (tramite click del mouse, rotellina, ecc.), cliccare sui nodi per bloccarli e vederne una versione ingrandita che evidenzi i collegamenti, effettuare uno screenshot tramite fotocamera della struttura del grafo (usa la libreria html2canvas, non disponibile per Internet Explorer).
Il progetto è stato testato sui seguenti browser:
- Internet Explorer versione 11.592.18362.0
- Mozilla Firefox versione 72.0.2
- Google Chrome versione 79.0.3945.130
E su sistema operativo Windows 10
La versione di Python installata sul sistema e consigliata è la 3.8.1
Il vantaggio offerto dalle rappresentazioni con DH96 rispetto al force-directed consiste nel poter migliorare alcune metriche,
tra cui il numero di incroci, permettendo una migliore visibilità del grafo finale.
Rappresentando infatti lo stesso grafo di 52 nodi e 152 archi utilizzato come test:
- con approccio force directed in 20000 iterazioni si ottiene un numero di incroci fino ad un minimo di 1069 (aumentando il numero di iterazioni si finisce per peggiorare il disegno e
aumentare il numero di incroci)
- con l'approccio DH96 si arriva fino a 607 incroci con le iterazioni più lunghe.
Sarà quindi sufficiente impostare un cooling factor pari a 0.51 nel caso di test per avere rappresentazioni migliori dell'approccio force directed, per quanto più lunghe in termini di tempo.

Note: lo script dh.py tenterà di fare il download di alcuni moduli necessari alla sua esecuzione mediante pip, un proxy potrebbe impedirne
l'installazione
