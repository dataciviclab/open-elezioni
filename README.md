# open-elezioni — DataCivicLab

Dati elettorali e amministratori locali italiani, dalle fonti del Ministero
dell'Interno (DAIT):

- **Eligendo** — risultati elettorali dal 1946 (Camera, Senato, Europee,
  Regionali, Comunali, Referendum)
- **Anagrafe degli amministratori** — eletti locali e regionali (1986-oggi)
- **SUT** — anagrafica e codici territoriali (ISTAT, elettorali, Belfiore)

- **Stato:** alpha (scaffold)
- **Copertura:** elezioni 1964-2024, amministratori 1986-2025, territorio Italia
- **Unità di analisi:** comune / lista / candidato (elezioni); ente × carica (amministratori)

## La domanda civica

Come votano gli italiani, territorio per territorio, e chi viene eletto?
Il repo tiene insieme il **voto** (Eligendo) e gli **eletti** (amministratori),
con i **codici territoriali** (SUT) come chiave di join.

## Dataset

I dataset elettorali sono in **migrazione da `open-politica`** e verranno
spostati qui con la relativa pipeline.

| Slug | Cosa contiene | Anni | Stato |
|---|---|---|---|
| `elezioni-politiche` | Camera + Senato per comune | 1948-2022 | in migrazione |
| `elezioni-europee` | Europee per comune | 1979-2024 | in migrazione |
| `elezioni-regionali` | Regionali per comune | 1970-2024 | in migrazione |
| `elezioni-comunali` | Comunali per comune | 1964-2024 | in migrazione |
| `elezioni-referendum` | Referendum per comune/quesito | 1974-2022 | in migrazione |
| `dait-amministratori-locali` | amministratori in carica | 2026 | in migrazione |
| `dait-amministratori-storico` | amministratori 31/12 | 1986-2025 | in migrazione |

Definizioni dettagliate: [`docs/data_dictionary.md`](docs/data_dictionary.md)

## Support dataset

Le anagrafiche condivise vivono in `support/` e si eseguono con `make seeds`.

| Slug | Cosa contiene | Uso |
|---|---|---|
| `sut-codici-comuni` | codici ISTAT, elettorali e Belfiore dei comuni | lookup per i join territoriali |

## Perché fidarsi

- fonti ufficiali DAIT ([`docs/sources.md`](docs/sources.md))
- trasformazioni documentate ([`docs/decisions.md`](docs/decisions.md))
- controlli automatici prima della pubblicazione (CI + contract test)

## Comandi

```bash
make seeds   # support dataset (SUT)
make run     # dataset principali
make check   # preflight config
make registry-write  # rigenera registry/
```

## Confine con il toolkit

Il motore della pipeline vive nel repository `toolkit`. Questa repo definisce
input, regole e output attesi per ogni dataset; non replica la logica di
esecuzione.
