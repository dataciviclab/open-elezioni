# elezioni-comunali

Risultati delle elezioni comunali in Italia per comune, candidato e lista (1964-2026).

**Fonte**: Eligendo — Archivio storico elettorale del DAIT (Ministero dell'Interno)
**Licenza**: dati pubblici

## Domanda guida

Come si distribuisce il voto alle elezioni comunali nei comuni italiani? Quali candidati e liste vincono?

## Dataset

- **Copertura**: 1964–2026 (42 anni, 162 tornate)
- **Granularità**: comunale per candidato, lista e turno
- **Righe**: ~326.000
- **Colonne**: 15 (data_elezione, regione, provincia, comune, turno, candidato, lista, voti_candidato, voti_lista, ...)
- **Comuni coperti**: varia per tornata (scadenze mandato)

## Stato

`candidate` — run verificato su 42 annualità.

## Gap noti
- 2024-11-17 e 2025 (3 tornate): formato per sezione (ListeLivSez XLSX + Scrutini per sezione), parser dedicato da fare
