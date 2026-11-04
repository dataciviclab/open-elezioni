# sut-comuni-bridge

Bridge per collegare i dataset elettorali ai comuni tramite codice ISTAT.

**Fonte**: DAIT — SUT open data
- https://dait.interno.gov.it/territorio-e-autonomie-locali/indice-sut/open-data/elenco-codici-comuni-csv.php
- https://dait.interno.gov.it/territorio-e-autonomie-locali/indice-sut/open-data/elenco-sezioni-csv.php

**Licenza**: CC BY 4.0

## Perché esiste

I dataset Eligendo in `open-politica` hanno `regione`, `provincia`, `comune`
come **nomi**, senza codice ISTAT. `sut-codici-comuni` ha il codice ma non i
nomi di regione/provincia; `elenco-sezioni` li ha. Questo support unisce i due
e produce una riga per comune con chiavi normalizzate.

## Colonne

| Colonna | Note |
|---|---|
| `comune`, `sigla`, `regione`, `provincia` | valori come da fonte |
| `codice_istat` | 6 cifre (da `="028001"`) |
| `codice_belfiore` | catastale |
| `codice_elettorale` | 10 cifre = `1` + `codice_dait_completo` (9 cifre) |
| `comune_norm`, `provincia_norm`, `regione_norm` | `UPPER(TRIM(...))` per i join |

## Join tipico

I dataset Eligendo hanno `regione/provincia/comune` come **nomi**, spesso in
casing misto. La chiave robusta è `comune_norm`; la provincia va usata solo
come disambiguazione.

```sql
FROM op
LEFT JOIN read_parquet('{support.sut_comuni.mart}') s
  ON UPPER(TRIM(op.comune)) = s.comune_norm
```

Solo 5 nomi di comune sono ambigui in Italia (`CASTRO`, `LIVO`, `PEGLIO`,
`SAMONE`, `SAN TEODORO`): per quelli aggiungere la provincia o un override.

**Non** usare `(comune, provincia)` come chiave unica: le province dei dataset
storici hanno nomi diversi dallo snapshot SUT (es. `VERBANIA` /
`VERB.-CUS.OSSOLA` / `VERBANO-CUSIO-OSSOLA`, `FORLI` / `FORLI'` /
`FORLI'-CESENA` / `RIMINI`, `CAGLIARI` / `SUD SARDEGNA`). Il match scende da
~91% (solo comune) a ~78% (comune+provincia).

## Limiti

- snapshot **corrente** (7.894 comuni): i comuni soppressi/fusi prima del 2009
  non sono coperti; il match storico è ~91%.
- le province storiche cambiano nome: non usarle come chiave di join.
- usare sempre `LEFT JOIN` e tenere la riga anche quando `codice_istat` è NULL.

