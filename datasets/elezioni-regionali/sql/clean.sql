WITH base AS (
    SELECT
        TRY_CAST(data_elezione AS DATE) AS data_elezione,
        normalize_string(regione) AS regione,
        normalize_string(circoscrizione) AS circoscrizione,
        normalize_string(provincia) AS provincia,
        normalize_string(comune) AS comune,
        cast_bigint(elettori) AS elettori,
        cast_bigint(votanti) AS votanti,
        cast_bigint(schede_bianche) AS schede_bianche,
        normalize_string(candidato) AS candidato,
        cast_bigint(voti_candidato) AS voti_candidato,
        normalize_string(lista) AS lista,
        cast_bigint(voti_lista) AS voti_lista
    FROM raw_input
),
sut AS (
    SELECT codice_istat, codice_belfiore, codice_elettorale, comune_norm
    FROM read_parquet('{support.sut_comuni.mart}')
)
SELECT
    base.*,
    sut.codice_istat,
    sut.codice_belfiore,
    sut.codice_elettorale,
    sut.codice_istat IS NOT NULL AS match_sut
FROM base
LEFT JOIN sut ON UPPER(TRIM(base.comune)) = sut.comune_norm
