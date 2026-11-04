# Datasets

Un dataset per directory, ognuna con `dataset.yml`, `sql/` e — se serve —
`preprocess.py`.

## Elettorali (Eligendo)

- `elezioni-politiche` — Camera + Senato, 1948-2022
- `elezioni-europee` — 1979-2024
- `elezioni-regionali` — 1970-2024
- `elezioni-comunali` — 1964-2024
- `elezioni-referendum` — 1974-2022
- `elezioni-provinciali` — 2004-2011

## Amministratori (DAIT)

- `dait-amministratori-locali` — snapshot 2026
- `dait-amministratori-storico` — 1986-2025

## Codice condiviso

`datasets/_shared/eligendo.py` — download ZIP, selezione entry, lettura
CSV/TXT/XLSX e merge, usati dai preprocess.
