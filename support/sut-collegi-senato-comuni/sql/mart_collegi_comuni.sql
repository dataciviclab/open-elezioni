-- Mapping comune -> collegi Senato.
SELECT
    comune_norm,
    sigla_norm,
    comune,
    sigla_provincia,
    circoscrizione_regionale,
    collegio_plurinominale,
    collegio_uninominale
FROM clean_input
