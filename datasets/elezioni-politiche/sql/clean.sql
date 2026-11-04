WITH base AS (
    SELECT
        TRY_CAST(data_elezione AS DATE) AS data_elezione,
        normalize_string(camera_senato) AS camera_senato,
        normalize_string(circoscrizione) AS circoscrizione,
        normalize_string(provincia) AS provincia,
        normalize_string(comune) AS comune,
        normalize_string(collegio_plurinominale) AS collegio_plurinominale,
        normalize_string(collegio_uninominale) AS collegio_uninominale,
        cast_bigint(elettori_totali) AS elettori_totali,
        cast_bigint(elettori_maschi) AS elettori_maschi,
        cast_bigint(votanti_totali) AS votanti_totali,
        cast_bigint(votanti_maschi) AS votanti_maschi,
        cast_bigint(schede_biache) AS schede_biache,
        normalize_string(lista) AS lista,
        cast_bigint(voti_lista) AS voti_lista,
        normalize_string(descr_lista) AS descr_lista,
        normalize_string(cognome) AS cognome,
        normalize_string(nome) AS nome,
        normalize_string(luogo_nascita) AS luogo_nascita,
        normalize_string(data_nascita) AS data_nascita,
        normalize_string(sesso) AS sesso,
        cast_bigint(voti_candidato) AS voti_candidato
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
