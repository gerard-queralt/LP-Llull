# Llull

Implementació de Llull feta per Gerard Queralt Ferré, basada en [l'especificació de l'enunciat][Enunciat].

## Set-up

Executeu aquesta comanda per compilar la gramàtica i crear els arxius necessaris:

```bash
antlr4 -Dlanguage=Python3 -no-listener -visitor llull.g4
```

Executeu aquesta comanda per instal·lar les dependències dels visitadors:

```bash
pip3 install -r requirements.txt
```

## Especificació de Llull

Aquesta implementació inclou extensions respecte l'especificació de l'enunciat. Només documentaré les extensions; l'especificació base es pot trobar [aquí][Enunciat].

### Potències

L'operador de potència `^` té associativitat per la dreta, com és d'esperar.

### Lectura

La lectura funciona com diu l'especificació, amb un parell d'extensions. En primer lloc, es mostra per pantalla el nom de la variable seguit de `=`, per indicar a l'usuari que s'espera que introdueixi un paràmetre. Per exemple, la línia:

```
read(a)
```

Mostra per pantalla:

```
a = 
```

En segon lloc es permeten múltiples lectures amb una sola crida. És a dir, el codi:

```
read(a)
read(b)
read(c)
```

Es pot simplificar com:

```
read(a, b, c)
```

Similar a com `write` permet múltiples escriptures.

### Taules

Com que no s'especifica a l'enunciat, les taules poden contenir qualsevol element, sigui un enter o una altra taula, i no tots els elements han de tenir el mateix tipus.

### And, Or i Not

Els operadors `&&`, `||` i `!` funcionen com es pot esperar de qualsevol llenguatge de programació, amb la diferència de que, com que Llull no té tipus booleà, funcionen amb enters.

### If, else, while i for

L'especificació de Llull inclou aquestes estructures de control, però aquesta implementació permet no afegir les claus dels blocs si només són d'una línia.

### Assignació composta

Com la majoria de llenguatges de programació, aquesta implementació de Llull permet fer assignacions compostes. Per tant, enlloc de fer:

```
a = a + 1
```

Es pot fer:

```
a += 1
```

Funciona amb tots els operadors aritmètics disponibles en el llenguatge: `+`, `-`, `*`, `/`, `%` i `^`.

## Continguts

En aquest zip hi trobaràs:

- Un fitxer `requirements.txt` amb les dependències dels visitadors.
- Un fitxer `llull.g4` amb la gramàtica del llenguatge Llull.
- Un fitxer `llull.py` amb el programa de l'intèrpret.
- Un fitxer `EvalVisitor.py` amb el programa del visitador de l'intèrpret.
- Un fitxer `beat.py` amb el programa del *pretty-printer*.
- Un fitxer `PrinterVisitor.py` amb el programa del visitador del *pretty-printer*
- Fitxers `test-<extensió>.llull`, on `<extensió>` és l'extensió del llenguatge que testeja el codi.
- Aquest `README.md`.

## Com utilitzar

L'extensió de tots els fitxers ha de ser `.llull`

### Intèrpret

L'intèrpret de Llull s'invoca amb la comanda

```bash
python3 llull.py <nom del fitxer>
```

Per defecte l'intèrpret invocarà la funció `main` del codi, però podem canviar la funció principal i passar-li arguments

```bash
python3 llull.py <nom del fitxer> <nom de la funció> <argument 1> <argument 2> ...
```

### *Pretty-printer*

El *pretty-printer* de Llull s'invoca amb la comanda

```bash
python3 beat.py <nom del fitxer>
```

El resultat és el codi del fitxer formatejat segons [l'enunciat][Enunciat]

[Enunciat]: https://github.com/jordi-petit/lp-llull-2021
# LP-Llull
