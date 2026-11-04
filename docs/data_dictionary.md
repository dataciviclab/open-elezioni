# Data Dictionary

Audience: Maintainers

Schema dei dataset del repo. I dataset elettorali sono in migrazione da
`open-politica`; qui è documentato il support dataset già attivo.

## support/sut-codici-comuni

### Clean

| Column | Type | Description | Nullable | Validation |
| --- | --- | --- | --- | --- |
| `nr` | BIGINT | numero riga della fonte | sì | — |
| `comune` | VARCHAR | denominazione comune | no | not_null |
| `sigla` | VARCHAR | sigla provincia | no | not_null |
| `codice_elettorale` | VARCHAR | codice elettorale DAIT (10 cifre) | sì | — |
| `codice_istat` | VARCHAR | codice ISTAT comune (6 cifre) | no | primary_key, not_null |
| `codice_belfiore` | VARCHAR | codice catastale/Belfiore | no | not_null |

### Mart

| Column | Type | Description | Nullable | Consumer |
| --- | --- | --- | --- | --- |
| `codice_istat` | VARCHAR | chiave comune | no | join dataset elettorali |
| `comune` | VARCHAR | denominazione | no | report/dashboard |
| `sigla` | VARCHAR | sigla provincia | no | aggregazioni |
| `codice_belfiore` | VARCHAR | codice catastale | no | join anagrafiche |
| `codice_elettorale` | VARCHAR | codice elettorale | sì | join fonti Eligendo |

## dataset in migrazione

Gli schemi di `elezioni-*` e `dait-amministratori-*` sono documentati nei
rispettivi README/notes in `open-politica` e verranno portati qui con la
migrazione.
