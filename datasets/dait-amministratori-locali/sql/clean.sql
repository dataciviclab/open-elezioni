WITH base AS (
    -- Clean: dait_amministratori_locali
    -- Fonte: ammcom.csv + ammprov.csv + ammreg.csv (DAIT — Ministero dell'Interno)
    -- Skip 2 righe di metadati gestito in dataset.yml (clean.read.skip: 2)
    -- Encoding UTF-8, delim ; — union_by_name unisce i 3 CSV (colonne mancanti → NULL)
    -- livello_ente iniettato da inject_column in dataset.yml
    -- Date in formato DD/MM/YYYY — parsate da DuckDB via clean.read.dateformat
    --
    -- Colonna "lista_appartenenza/collegamento" rinominata in SQL
    -- denominazione_{comune,provincia,regione} unificata in denominazione_ente
    -- popolazione_censita e codice_dait_completo valorizzati solo per livello comune
    -- data_elezione_max_carica presente solo per livello provincia
    --
    -- Codici territoriali (codice_regione/provincia/comune) mantenuti come VARCHAR
    -- per preservare il leading zero. DAIT usa un proprio sistema di codifica
    -- comunale (codice_comune a 4 cifre, non 3 come ISTAT): la concatenazione
    -- regione(2)+provincia(3)+comune(4) genera codice_dait_completo (9 caratteri).
    -- Non e' un codice ISTAT — serve una mappatura verificata per join con dataset
    -- ISTAT o BDAP.
    
    SELECT
        cast_int({year})                                       AS anno,
        livello_ente                                          AS livello_ente,
        normalize_string(codice_regione)                            AS codice_regione,
        normalize_string(codice_provincia)                          AS codice_provincia,
        normalize_string(codice_comune)                             AS codice_comune,
        -- codice_dait_completo ha senso solo a livello comune (9 cifre)
        CASE WHEN livello_ente = 'comune'
             THEN normalize_string(codice_regione || codice_provincia || codice_comune)
        END                                                   AS codice_dait_completo,
        -- denominazione unificata: comune > provincia > regione
        COALESCE(
            normalize_string(denominazione_comune),
            normalize_string(denominazione_provincia),
            normalize_string(denominazione_regione)
        )                                                     AS denominazione_ente,
        normalize_string(sigla_provincia)                           AS sigla_provincia,
        -- popolazione censita disponibile solo a livello comune
        -- (auto-detect la tipizza BIGINT; vuoti → NULL nativo)
        CASE WHEN livello_ente = 'comune'
             THEN cast_int(popolazione_censita_alla_data_elezione)
        END                                                   AS popolazione_censita,
        cognome                                               AS cognome,
        nome                                                  AS nome,
        sesso                                                 AS sesso,
        data_nascita                                          AS data_nascita,
        luogo_nascita                                         AS luogo_nascita,
        descrizione_carica                                    AS descrizione_carica,
        normalize_string(incarico)                                  AS incarico,
        data_elezione                                         AS data_elezione,
        data_entrata_in_carica                                AS data_entrata_in_carica,
        -- solo livello provincia
        data_elezione_max_carica                              AS data_elezione_max_carica,
        normalize_string("lista_appartenenza/collegamento")         AS lista_appartenenza,
        normalize_string(titolo_studio)                             AS titolo_studio,
        normalize_string(professione)                               AS professione
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
LEFT JOIN sut ON SUBSTR(sut.codice_elettorale, 2) = base.codice_dait_completo
