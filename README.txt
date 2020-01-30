Il seguente progetto utilizza un server in Python costruito con il modulo flask.
A partire dalla pagina principale index.html viene selezionato un file contenente il grafo in formato json o graphml e sono impostati una serie di parametri.
Premendo ok vengono mandate delle richieste Ajax al server, che elabora il grafo generando le posizioni per i nodi.
La risposta restituita dal server viene infine visualizzata utilizzando d3.js
