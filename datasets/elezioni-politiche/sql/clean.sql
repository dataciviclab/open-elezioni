WITH base AS (
    SELECT
        TRY_CAST(data_elezione AS DATE) AS data_elezione,
        CAST(camera_senato AS VARCHAR) AS camera_senato,
        CAST(circoscrizione AS VARCHAR) AS circoscrizione,
        CAST(provincia AS VARCHAR) AS provincia,
        CAST(comune AS VARCHAR) AS comune,
        CAST(collegio_plurinominale AS VARCHAR) AS collegio_plurinominale,
        CAST(collegio_uninominale AS VARCHAR) AS collegio_uninominale,
        TRY_CAST(elettori_totali AS BIGINT) AS elettori_totali,
        TRY_CAST(elettori_maschi AS BIGINT) AS elettori_maschi,
        TRY_CAST(votanti_totali AS BIGINT) AS votanti_totali,
        TRY_CAST(votanti_maschi AS BIGINT) AS votanti_maschi,
        TRY_CAST(schede_biache AS BIGINT) AS schede_biache,
        CAST(lista AS VARCHAR) AS lista,
        TRY_CAST(voti_lista AS BIGINT) AS voti_lista,
        CAST(descr_lista AS VARCHAR) AS descr_lista,
        CAST(cognome AS VARCHAR) AS cognome,
        CAST(nome AS VARCHAR) AS nome,
        CAST(luogo_nascita AS VARCHAR) AS luogo_nascita,
        CAST(data_nascita AS VARCHAR) AS data_nascita,
        CAST(sesso AS VARCHAR) AS sesso,
        TRY_CAST(voti_candidato AS BIGINT) AS voti_candidato
    FROM raw_input
    WHERE
        TRY_CAST(data_elezione AS DATE) IS NOT NULL
        AND camera_senato IN ('C', 'S')
        AND comune IS NOT NULL
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
