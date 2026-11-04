# sut-collegi-camera-comuni

Mapping tra comuni e collegi **Camera** (plurinominale/uninominale), dal SUT.

**Fonte**: https://dait.interno.gov.it/territorio-e-autonomie-locali/indice-sut/open-data/elenco-collegi-camera-comuni-csv.php
**Riferimento**: D.Lgs. 23 dicembre 2020, n. 177 (Rosatellum)
**Licenza**: CC BY 4.0

## Uso

Collega `elezioni-politiche` (2018/2022) ai collegi. Per le elezioni
pre-2018 il sistema di collegi è diverso: non usare questo mapping.

Join consigliato:

```sql
LEFT JOIN read_parquet('{support.sut_collegi_camera.mart}') c
  ON UPPER(TRIM(op.comune)) = c.comune_norm
 AND UPPER(TRIM(op.provincia)) = c.sigla_norm
```

## Note

- prima riga del CSV = titolo (`D.Lgs. 177/2020`); `skip: 1`
- 7.907 righe (comune × collegio uninominale)
