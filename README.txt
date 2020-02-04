Il seguente progetto utilizza un server in Python costruito con il modulo flask.
A partire dalla pagina principale index.html è possibile selezionare un file contenente un grafo in formato json o graphml [nodes: id, type, name| links: source, target], impostando una serie di parametri a seconda dell'estetica che si preferisce valorizzare maggiormente (distanza tra nodi, lunghezza degli archi, numero di incroci), seguendo le linee guida dell'algoritmo proposto da Davidson e Harel nel 1996.
Premendo il bottone "genera il grafo" viene mandata una richiesta Ajax al server, che elabora il grafo generando le posizioni per i nodi.
La risposta restituita dal server viene infine visualizzata utilizzando d3.js
A partire dal grafo visualizzato è possibile spostarlo trascinandolo con il mouse, effettuare lo zoom (tramite click del mouse, rotellina, ecc.), cliccare sui nodi per bloccarli e vederne una versione ingrandita che evidenzi i collegamenti, effettuare uno screenshot tramite fotocamera della struttura del grafo (usa la libreria html2canvas, non disponibile per Internet Explorer).
Il progetto è stato testato sui seguenti browser:
- Internet Explorer versione 11.592.18362.0
- Mozilla Firefox versione 72.0.2
- Google Chrome versione 79.0.3945.130
E su sistema operativo Windows
