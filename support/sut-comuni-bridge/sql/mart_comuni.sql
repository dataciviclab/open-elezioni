-- Lookup comuni: una riga per comune, chiave codice_istat.
SELECT
    codice_istat,
    comune,
    comune_norm,
    sigla,
    regione,
    regione_norm,
    provincia,
    provincia_norm,
    codice_belfiore,
    codice_elettorale
FROM clean_input
