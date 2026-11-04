-- Lookup comuni: UNA riga per comune_norm (chiave di join unica).
-- Per i 5 nomi omonimi (ambiguous) il codice resta NULL: meglio nessun
-- codice che un codice sbagliato. Il flag `ambiguous` lo segnala.
SELECT
    comune_norm,
    MAX(ambiguous::INT)::BOOLEAN AS ambiguous,
    MAX(CASE WHEN NOT ambiguous THEN codice_istat END) AS codice_istat,
    MAX(CASE WHEN NOT ambiguous THEN codice_belfiore END) AS codice_belfiore,
    MAX(CASE WHEN NOT ambiguous THEN codice_elettorale END) AS codice_elettorale,
    MAX(sigla) AS sigla,
    MAX(regione) AS regione,
    MAX(regione_norm) AS regione_norm,
    MAX(provincia) AS provincia,
    MAX(provincia_norm) AS provincia_norm
FROM clean_input
GROUP BY comune_norm
