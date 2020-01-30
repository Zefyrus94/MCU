Il seguente progetto utilizza un server in Python costruito con il modulo flask.
A partire dalla pagina principale index.html è possibile selezionare un file contenente un grafo in formato json o graphml [nodes: id, type, name| links: source, target], impostando una serie di parametri a seconda dell'estetica che si preferisce valorizzare maggiormente (distanza tra nodi, lunghezza tra gli archi, numero di incroci), seguendo le linee guida dell'algoritmo proposto da Davidson e Harel nel 1996.
Premendo il bottone "genera il grafo" viene mandata una richiesta Ajax al server, che elabora il grafo generando le posizioni per i nodi.
La risposta restituita dal server viene infine visualizzata utilizzando d3.js
