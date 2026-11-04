-- Bridge comuni SUT: una riga per comune.
-- Le chiavi normalizzate (upper+trim) servono ai join dei dataset elettorali,
-- che hanno nomi in casing misto (es. "Cuneo" vs "CUNEO").
SELECT
    normalize_string(comune) AS comune,
    normalize_string(sigla) AS sigla,
    normalize_string(regione) AS regione,
    normalize_string(provincia) AS provincia,
    NULLIF(trim(codice_istat), '') AS codice_istat,
    NULLIF(trim(codice_belfiore), '') AS codice_belfiore,
    NULLIF(trim(codice_elettorale), '') AS codice_elettorale,
    UPPER(TRIM(comune)) AS comune_norm,
    UPPER(TRIM(provincia)) AS provincia_norm,
    UPPER(TRIM(regione)) AS regione_norm
FROM raw_input
