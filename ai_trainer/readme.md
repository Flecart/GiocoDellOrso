## Come allenare l'ai 

questa è la directory con tutti i file utilizzati per allenare l'ai.
per allenarlo basta runnare `bash start.sh`, oppure eseguire direttamente il comando per far partire l'allenamento. 

Per sapere i comandi runnare `python3 controller.py -h`

### Alcuni esempi su come allenare:

Ad ogni allenamento corrisponderanno un output in pickle fatto in una struttura del genere:
`bear_[timestamp].policy`, e `hunter_[timestamp].policy`, così non va a sovrascrivere la
policy vecchia.

- Allena sia hunter che bear da 0 per 10000 partite
  - `python3 controller.py --n_games 10000`
- Allena per un numero default di partite caricando da un file
  - `python3 controller.py --bear_ai_file [nome_file_bear]`
- Gioca come human come bear (disabilitando l'allenamento)
  - `python3 controller.py --bear_human --disable_training --display_board`
  - Con questa opzione saranno printate su terminale interfaccia per giocare al gioco dell'orso
- Per altri comandi consultare `python3 controller.py -h`

## La versione in orso_ai 
esiste una versione che è uscita dopo ore di allenamento (quindi qualche milioncino di partite) che sembra giocare molto bene, è il `bear_v2.policy`. 

### Note
Quella versione è stata prodotta con codice differente rispetto a questa versione che di cui sto facendo PR, ma ritengo quel codice non molto comprensibile (scritta velocemente, come veniva veniva), per questo motivo preferisco mostrare questo codice in quanto fatto per essere letto e mantenuto. 

In ogni modo se curiosi della versione originale, è presente nella branch master nel mio fork

### Esempi:

`python3 controller.py --hunter_human --disable_training --display_board --bear_ai_file bear_1675023175.policy `

Vuol dire gioca come umano, mostra la mappa di gioco (necessaria se vuoi giocare come umano credo xD, altrimenti te li tieni a memoria ahah), caricando un file di training, e disabilitando l'esplorazione da parte dall'AI (l'esplorazione serve se vuoi imparare qualcosa!)