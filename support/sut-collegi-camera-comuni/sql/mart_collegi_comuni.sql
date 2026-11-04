-- Mapping comune -> collegi Camera.
SELECT
    comune_norm,
    sigla_norm,
    comune,
    sigla_provincia,
    circoscrizione,
    collegio_plurinominale,
    collegio_uninominale
FROM clean_input
