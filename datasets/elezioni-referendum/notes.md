# elezioni-referendum

## Issue
DataCivicLab/dataset-incubator#633

## Fonte dati
Eligendo — https://elezionistorico.interno.gov.it/
Open data DAIT: https://dait.interno.gov.it/elezioni/open-data

## Schema raw
Colonne variabili per anno (normalizzate via COL_MAP regex):
- regione, provincia, comune, num_quesito, quesito, elettori, votanti, voti_si, voti_no, schede_bianche, ...

## Gap noti
- 1974, 1978, 1981, 1985: livello comunale
- 1987-2006: livello provinciale (colonna comune NULL)
- 2009 in poi: livello comunale
- 1985: ZIP senza riga di intestazione → schema posizionale `HEADERLESS_COLS`
- 1989 e 1991: un solo quesito su 95 province (per questo `min_rows` = 90)
- 2001: solo referendum costituzionale (Titolo V) — diverso dagli abrogativi
- 1946 (referendum istituzionale monarchia/repubblica): escluso, la fonte usa
  31 CIRCOSCRIZIONI senza REGIONE → candidato separato
- 2025 e 2026: inclusi; i ZIP sono stati ripubblicati in CSV (2025 con
  LivComune, 2026 LivComune con riga di titolo prima dell'header). Il parsing
  sceglie LivComune, salta il titolo e calcola `voti_no` = validi − sì quando
  la fonte non lo porta.
- Perimetro 2025/2026: **solo comuni italiani**. Il voto estero
  (`Referendum*_EsteroNazione.csv`, 2026: 181 righe, 1.563.377 votanti,
  803.632 sì) e' escluso: usa `RIPARTIZIONE`/`NAZIONE`, non
  regione/provincia/comune, e senza esclusione entrerebbero righe con comune
  vuoto. Il clean non copre quindi il voto dall'estero.
- 1995: tre quesiti hanno codice alfabetico (A, D, E); `clean.sql` casta
  `num_quesito` a BIGINT e nel clean restano NULL (i voti sono presenti).
  Il conteggio dei quesiti distinti nel clean e' quindi 79: i tre codici
  alfabetici del 1995 non entrano nel conteggio.

## Note
- I quesiti multipli per anno hanno lo stesso num_quesito per tutti i comuni
- I totali voti SI+NO nei dati sono la somma per tutti i quesiti dell'anno
