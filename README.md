# open-elezioni — Il voto e gli eletti, comune per comune

[![check](https://github.com/dataciviclab/open-elezioni/actions/workflows/check.yml/badge.svg)](https://github.com/dataciviclab/open-elezioni/actions/workflows/check.yml)

**Come vota l'Italia, territorio per territorio? E chi viene eletto?**

open-elezioni raccoglie i dati ufficiali del Ministero dell'Interno (DAIT):
risultati elettorali **Eligendo** dal 1948 e **Anagrafe degli amministratori**
locali. Li puliamo, li colleghiamo ai codici ISTAT e li pubblichiamo come
parquet interrogabili.

## Cosa contiene

| Dataset | Cosa contiene | Periodo | Righe |
|---|---|---|---:|
| `elezioni_politiche` | Camera + Senato per comune | 1948-2022 (19 tornate) | ~3,78M |
| `elezioni_europee` | Europee per comune | 1979-2024 (10 tornate) | ~1,2M |
| `elezioni_regionali` | Regionali per comune | 1970-2024 (28 tornate) | ~962k |
| `elezioni_comunali` | Comunali per comune, lista e candidato | 1964-2024 (160 tornate) | ~323k |
| `elezioni_referendum` | Referendum per comune e quesito | 1974-2022 (23 tornate) | ~198k |
| `dait_amministratori_locali` | amministratori in carica | 2026 | 127.805 |
| `dait_amministratori_storico` | amministratori al 31/12 | 1986-2025 | 6.075.430 |

**Copertura**: ~7.900 comuni, 20 regioni, 98 province. I dataset elettorali
espongono `codice_istat`, `codice_belfiore`, `codice_elettorale` e `match_sut`
per collegare voto, eletti e territorio.

### Support

| Dataset | Cosa contiene |
|---|---|
| `sut_codici_comuni` | codici ISTAT, Belfiore ed elettorali dei comuni |
| `sut_comuni_bridge` | codici + regione/provincia + chiavi normalizzate |
| `sut_collegi_camera_comuni` / `sut_collegi_senato_comuni` | comune → collegio |

## Esempi di domande

- **Come è cambiata l'affluenza dal 1948 a oggi?**
- **Quali comuni hanno votato più SI al referendum del 2016?**
- **Chi è il sindaco del tuo comune e quanti consiglieri ha?**
- **Quante donne sono elette nei consigli comunali dal 1986?**
- **Come vota Torino rispetto a Napoli?**

## Tre modi per accedere

### 1. Via MCP (Lab)

- `gcs_query(slug, sql)` — SQL sui parquet pubblicati
- `toolkit_find` / `toolkit_dataset_overview` — scoperta e schema
- `toolkit_registry_show repo=open-elezioni` — catalogo e stato run

### 2. Via DuckDB

```python
import duckdb
duckdb.sql("""
    SELECT anno, SUM(voti_lista) AS voti
    FROM read_parquet('gs://dataciviclab-clean/open-elezioni/elezioni_regionali/*/*.parquet')
    WHERE comune = 'TORINO'
    GROUP BY anno ORDER BY anno
""").show()
```

### 3. Via parquet

Bucket pubblico: `gs://dataciviclab-clean/open-elezioni/` (clean) e
`gs://dataciviclab-mart/open-elezioni/` (mart), accessibili anche via HTTPS.

## Approfondimenti

- [Discussions](https://github.com/dataciviclab/open-elezioni/discussions)
- Schema e fonti: [`docs/data_dictionary.md`](docs/data_dictionary.md) · [`docs/sources.md`](docs/sources.md)

## Partecipa

- **Hai una domanda sui dati?** Apri una [Discussion](https://github.com/dataciviclab/open-elezioni/discussions/new?category=Q-A)
- **Vuoi contribuire?** Vedi [CONTRIBUTING.md](CONTRIBUTING.md)

## Licenza

Codice MIT — vedi [LICENSE](LICENSE). Dati: CC BY 4.0 (DAIT).

Questo progetto fa parte di [DataCivicLab](https://github.com/dataciviclab).
