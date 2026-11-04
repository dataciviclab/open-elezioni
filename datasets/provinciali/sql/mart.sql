-- Mart: voti per lista e collegio/comune (provinciali 2004-2011).
SELECT
    data_elezione,
    EXTRACT(YEAR FROM data_elezione) AS anno,
    regione,
    provincia,
    collegio,
    comune,
    lista,
    candidato,
    SUM(voti_lista) AS tot_voti_lista,
    MAX(voti_candidato) AS voti_candidato,
    MAX(elettori) AS elettori,
    MAX(votanti) AS votanti,
    MAX(schede_bianche) AS schede_bianche
FROM clean_input
GROUP BY data_elezione, regione, provincia, collegio, comune, lista, candidato
