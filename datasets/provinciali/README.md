# elezioni-provinciali

Risultati delle elezioni provinciali italiane (2004-2011), per collegio,
comune, lista e candidato.

**Fonte**: Eligendo — Archivio storico elettorale del DAIT
**Licenza**: CC BY 4.0

## Dataset

- **Copertura**: 2004–2011 (10 tornate)
- **Granularità**: collegio/comune × lista × candidato × turno
- **Colonne**: data_elezione, regione, provincia, collegio, comune, turno,
  candidato, lista, voti_candidato, voti_lista, elettori, votanti, ...
  + `codice_istat`, `codice_belfiore`, `codice_elettorale`, `match_sut` (SUT)

## Note

- Le elezioni provinciali sono state abolite/superate dalla riforma
  costituzionale (legge Delrio, 2014); la serie si ferma al 2011.
- Il campo `COMUNE` della fonte è il comune; in alcuni casi contiene il nome
  del collegio (es. `ACQUI TERME I`), che non matcha il SUT.
- `match_sut` indica se il comune è stato agganciato allo snapshot SUT.

## Mart

- `mart_voti_lista_collegio` — voti per lista × collegio/comune
