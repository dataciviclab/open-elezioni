-- Bridge comuni SUT: una riga per comune.
-- Le chiavi normalizzate (upper+trim) servono ai join dei dataset elettorali,
-- che hanno nomi in casing misto (es. "Cuneo" vs "CUNEO").
-- `ambiguous` = il nome comune esiste in più province: il join deve usare
-- anche la provincia per non duplicare le righe.
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
    UPPER(TRIM(regione)) AS regione_norm,
    COUNT(*) OVER (PARTITION BY UPPER(TRIM(comune))) > 1 AS ambiguous
FROM raw_input
