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

## support/sut-comuni-bridge

### Clean

| Column | Type | Description | Nullable | Validation |
| --- | --- | --- | --- | --- |
| `comune` | VARCHAR | denominazione comune | no | not_null |
| `sigla` | VARCHAR | sigla provincia | no | not_null |
| `regione` | VARCHAR | nome regione | no | not_null |
| `provincia` | VARCHAR | nome provincia | no | not_null |
| `codice_istat` | VARCHAR | codice ISTAT (6 cifre) | no | primary_key, not_null |
| `codice_belfiore` | VARCHAR | codice catastale | no | not_null |
| `codice_elettorale` | VARCHAR | `1` + codice DAIT 9 cifre | sì | — |
| `comune_norm` | VARCHAR | `UPPER(TRIM(comune))` | sì | chiave di join |
| `provincia_norm` | VARCHAR | `UPPER(TRIM(provincia))` | sì | disambiguazione |
| `regione_norm` | VARCHAR | `UPPER(TRIM(regione))` | sì | aggregazioni |

### Mart

| Column | Type | Description | Consumer |
| --- | --- | --- | --- |
| `codice_istat` | VARCHAR | chiave comune | join dataset elettorali |
| `comune_norm` | VARCHAR | chiave di join per nome | join `elezioni-*` |
| `regione`, `provincia`, `sigla` | VARCHAR | territorio | report |
| `codice_belfiore`, `codice_elettorale` | VARCHAR | codici alternativi | join anagrafiche/DAIT |

## support/sut-collegi-camera-comuni e sut-collegi-senato-comuni

### Clean / Mart

| Column | Type | Description | Nullable |
| --- | --- | --- | --- |
| `comune` | VARCHAR | comune | no |
| `sigla_provincia` | VARCHAR | sigla provincia | no |
| `circoscrizione` / `circoscrizione_regionale` | VARCHAR | circoscrizione | sì |
| `collegio_plurinominale` | VARCHAR | collegio plurinominale | sì |
| `collegio_uninominale` | VARCHAR | collegio uninominale | no |
| `comune_norm`, `sigla_norm` | VARCHAR | chiavi normalizzate | sì |

Join: `elezioni-politiche` 2018/2022 (Rosatellum). Non usare per elezioni
pre-2018.

## dataset in migrazione


Gli schemi di `elezioni-*` e `dait-amministratori-*` sono documentati nei
rispettivi README/notes in `open-politica` e verranno portati qui con la
migrazione.

## Campi aggiunti dai support SUT

I 5 dataset `elezioni-*` e `dait-amministratori-locali` espongono in clean:

| Colonna | Note |
| --- | --- |
| `codice_istat` | NULL se il comune storico non è nello snapshot SUT |
| `codice_belfiore` | codice catastale |
| `codice_elettorale` | codice DAIT a 10 cifre |
| `match_sut` | `true` se il comune è stato agganciato al SUT |

`match_sut = false` non è un errore: sono i comuni soppressi/fusi che lo
snapshot corrente non contiene più.
