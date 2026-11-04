-- SUT/DAIT: elenco codici comuni italiani.
-- Fonte: SUT open data, CSV con delimitatore ';'.
-- Nota: CODICE ISTAT arriva in formato Excel `="028001"` → va ripulito.
SELECT
    TRY_CAST("NR." AS BIGINT) AS nr,
    normalize_string("DESCRIZIONE COMUNE") AS comune,
    normalize_string("SIGLA") AS sigla,
    normalize_string("CODICE ELETTORALE") AS codice_elettorale,
    NULLIF(replace(replace("CODICE ISTAT", '="', ''), '"', ''), '') AS codice_istat,
    normalize_string("CODICE BELFIORE") AS codice_belfiore
FROM raw_input
