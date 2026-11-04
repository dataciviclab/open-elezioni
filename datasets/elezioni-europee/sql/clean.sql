WITH base AS (
    SELECT
        CAST(data_elezione AS DATE) AS data_elezione,
        CAST(circoscrizione AS VARCHAR) AS circoscrizione,
        CAST(regione AS VARCHAR) AS regione,
        CAST(provincia AS VARCHAR) AS provincia,
        CAST(comune AS VARCHAR) AS comune,
        CAST(lista AS VARCHAR) AS lista,
        TRY_CAST(voti_lista AS BIGINT) AS voti_lista,
        TRY_CAST(elettori AS BIGINT) AS elettori,
        TRY_CAST(votanti AS BIGINT) AS votanti,
        TRY_CAST(schede_bianche AS BIGINT) AS schede_bianche
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
