-- Clean: dait_amministratori_storico
-- Fonte: preprocess.py → storico_amministratori.csv (serie 1986–2025)
-- Il preprocess ha già unificato le due ere schema e prodotto header
-- snake_case; qui si fa solo tipizzazione e normalizzazione valori.
--
-- Date in formato DD/MM/YYYY — parsate da DuckDB via clean.read.dateformat
-- Codici territoriali mantenuti come VARCHAR (leading zero).
-- codice_dait_completo = regione(2)||provincia(3)||comune(4) — non ISTAT.

SELECT
    cast_int(anno_snapshot)                                 AS anno_snapshot,
    normalize_string(codice_regione)                             AS codice_regione,
    normalize_string(descrizione_regione)                        AS descrizione_regione,
    normalize_string(codice_provincia)                           AS codice_provincia,
    normalize_string(descrizione_provincia)                      AS descrizione_provincia,
    normalize_string(codice_comune)                              AS codice_comune,
    normalize_string(descrizione_comune)                         AS descrizione_comune,
    normalize_string(codice_regione || codice_provincia || codice_comune)
                                                            AS codice_dait_completo,
    normalize_string(sigla_provincia)                            AS sigla_provincia,
    normalize_string(istat_codice_comune)                        AS istat_codice_comune,
    -- Auto-detect DuckDB tipizza i numerici (BIGINT) e le date (DATE);
    -- i vuoti diventano NULL nativamente — non serve NULLIF su stringhe.
    cast_int(popolazione_censita)                          AS popolazione_censita,
    normalize_string(maggioritario_proporzionale)                AS maggioritario_proporzionale,
    normalize_string(descrizione_tempo_gestione)                 AS descrizione_tempo_gestione,
    data_elezione                                          AS data_elezione,
    data_ballottaggio                                      AS data_ballottaggio,
    cast_int(consiglieri_spettanti)                         AS consiglieri_spettanti,
    cast_int(consiglieri_eletti)                            AS consiglieri_eletti,
    cast_int(assessori_assegnati)                           AS assessori_assegnati,
    normalize_string(cognome)                                    AS cognome,
    normalize_string(nome)                                       AS nome,
    normalize_string(sesso)                                      AS sesso,
    data_nascita                                           AS data_nascita,
    normalize_string(sede_nascita)                               AS sede_nascita,
    cast_int(livello_carica)                                AS livello_carica,
    normalize_string(descrizione_carica)                         AS descrizione_carica,
    data_inizio_carica                                     AS data_inizio_carica,
    data_cessazione                                        AS data_cessazione,
    normalize_string(incarico)                                   AS incarico,
    data_inizio_incarico                                   AS data_inizio_incarico,
    data_fine_incarico                                     AS data_fine_incarico,
    normalize_string(funzione)                                   AS funzione,
    data_inizio_funzione                                   AS data_inizio_funzione,
    data_fine_funzione                                     AS data_fine_funzione,
    normalize_string(lista_appartenenza)                         AS lista_appartenenza,
    normalize_string(titolo_studio)                              AS titolo_studio,
    normalize_string(professione)                                AS professione
FROM raw_input
