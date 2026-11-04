-- Lookup comuni: una riga per comune, chiave codice_istat.
SELECT
    codice_istat,
    comune,
    sigla,
    codice_belfiore,
    codice_elettorale
FROM clean_input
