## Come allenare l'ai 

questa è la directory con tutti i file utilizzati per allenare l'ai.
per allenarlo basta runnare `bash start.sh`, oppure eseguire direttamente il comando per far partire l'allenamento. 

Per sapere i comandi runnare `python3 controller.py -h`

### Come allenare:

`python3 controller.py --train`


In output troverai le states values, ossia una tabella di valutazione di ogni stato.
Il numero corrispondente allo stato è il minimo numero di mosse per vincere se entrambi
giocano nel modo ottimale.

### Note
Quella versione è stata prodotta con codice differente rispetto a questa versione che di cui sto facendo PR, ma ritengo quel codice non molto comprensibile (scritta velocemente, come veniva veniva), per questo motivo preferisco mostrare questo codice in quanto fatto per essere letto e mantenuto. 

In ogni modo se curiosi della versione originale, è presente nella branch master nel mio fork

### Esempi:

`python3 controller.py --hunter-human --bear-ai-file bear_1675023175.policy `

Vuol dire gioca come umano, mostra la mappa di gioco (necessaria se vuoi giocare come umano credo xD, altrimenti te li tieni a memoria ahah), caricando un file di training, e disabilitando l'esplorazione da parte dall'AI (l'esplorazione serve se vuoi imparare qualcosa!)