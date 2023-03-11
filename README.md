# Il Gioco Dell'Orso
Repository per varie versioni del gioco da tavolo dell'Orso (e del Cacciatore) per promuovere questo antico gioco giocato nelle Alpi italiane e da utilizzare come esercizio di Python



Il Gioco dell'Orso (e del Cacciatore) è un antico gioco da tavolo che si gioca in Valle del Cervo, nelle Alpi italiane

Maggiori informazioni sulla scoperta qui:
https://vallecervobiella.wordpress.com/il-gioco-dellorso/
 (in italiano)



## Regole del Gioco

* Il primo giocatore è il Cacciatore, possiede tre pedine nel tabellone con l'obiettivo di catturare (bloccare) l'orso in una delle dodici posizioni finali
* Il secondo giocatore è l'Orso, possiede un pedone unico; deve muoversi nel tabellone per 20/30/40 mosse senza essere bloccato in una delle posizioni finali, per poter fuggire e vincere



### Tavolo da gioco

* La tavola è un cerchio con un cerchio interno e quattro semicerchi, uno per ogni quarto, tutti divisi da due linee perpendicolari.
* Ogni intersezione è una posizione per i giocatori

## Aspetti progettuali ##

- `python3 controller.py [--hunter-human] [--bear-human]` se volete giocare con l'interfaccia di testo.
- `python3 controller.py --train` se volete avere in output le policies.

Se volete giocare con l'ai basta `--hunter-ai-file nome_file.policy` per caricare la policy dell'hunter.