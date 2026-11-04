# sut-codici-comuni

Anagrafica dei comuni italiani con i codici usati dalle procedure elettorali
e amministrative.

**Fonte**: DAIT — Sistema Unico Territoriale (SUT)
**URL**: https://dait.interno.gov.it/territorio-e-autonomie-locali/indice-sut/open-data/elenco-codici-comuni-csv.php
**Licenza**: CC BY 4.0

## Contenuto

- `codice_istat` — codice ISTAT del comune (6 cifre)
- `codice_belfiore` — codice catastale/Belfiore (4 caratteri)
- `codice_elettorale` — codice elettorale DAIT (10 cifre)
- `comune`, `sigla` — denominazione e sigla provincia

## Note tecniche

- CSV `;`, UTF-8, header in prima riga
- `CODICE ISTAT` in formato Excel `="028001"`: il clean rimuove `="` e `"`
- snapshot corrente (non storicizzato)
