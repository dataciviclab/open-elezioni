-- SUT/DAIT: comuni -> collegi Senato (Rosatellum, D.Lgs. 177/2020).
-- La prima riga del CSV e' un titolo: clean.read.skip = 1.
SELECT
    normalize_string("CIRCOSCRIZIONE REGIONALE") AS circoscrizione_regionale,
    normalize_string("COLLEGIO PLURINOMINALE") AS collegio_plurinominale,
    normalize_string("COLLEGIO UNINOMINALE") AS collegio_uninominale,
    normalize_string("COMUNE") AS comune,
    normalize_string("SIGLA PROVINCIA") AS sigla_provincia,
    UPPER(TRIM("COMUNE")) AS comune_norm,
    UPPER(TRIM("SIGLA PROVINCIA")) AS sigla_norm
FROM raw_input
