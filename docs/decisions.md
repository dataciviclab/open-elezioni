# Decision log

## D-001 — Repo dedicato alle elezioni (split da open-politica)

- decisione: spostare i dataset Eligendo e DAIT (amministratori) in
  `open-elezioni`, lasciando Camera/Senato in `open-politica`.
- motivo: fonti, protocolli e cadenze diverse; il repo parlamentare è già
  ~3/4 del volume; la famiglia elettorale crescerà (provinciali, assemblea,
  tornate recenti, SUT).
- impatto: nuovo prefisso GCS/registry `open-elezioni`; migrazione coordinata
  di registry, catalogo e data-explorer.
- alternative: riorganizzazione interna di `open-politica` (rinviata).

## D-002 — SUT come support dataset

- decisione: `sut-codici-comuni` è un support dataset (lookup), non un dataset
  principale.
- motivo: i codici ISTAT/Belfiore/elettorali servono ai join dei dataset
  elettorali; oggi i join avvengono per nome comune in maiuscolo.
- impatto: i dataset principali possono dichiarare il support e joinare per
  `codice_istat`.
- alternative: lookup locale duplicato nei singoli dataset (scartata).

## D-003 — Prefisso GCS/registry

- decisione: `repo-slug: open-elezioni` per GCS e registry.
- motivo: coerenza col nome del repo e leggibilità nel catalogo pubblico.
- impatto: i path passano da `gs://.../open-politica/<slug>/` a
  `gs://.../open-elezioni/<slug>/`; l'explorer legge il path dal registry.
- nota: i vecchi path restano orfani fino al cleanup.

## D-004 — Finanza locale fuori perimetro

- decisione: non includere la finanza locale DAIT.
- motivo: non è open data in bulk; è un'interfaccia HTML per singolo ente,
  senza export CSV/JSON. Richiederebbe un progetto di scraping separato.
- impatto: nessuno sui dataset elettorali.

## D-005 — Adattamento contract test del template

- decisione: `clean.validate.min_rows` è accettato come soglia `>= 1`
  (non forzato a 1) e `output.artifacts` è dichiarato esplicitamente.
- motivo: il support SUT ha 7.894 righe e vuole una soglia anti-vuoto reale
  (7.000), non 1; il test del template era più rigido del runtime.
- impatto: solo `tests/test_contract.py` locale; nessun cambio al toolkit.

## D-006 — Strategia di join col bridge SUT

- decisione: joinare i dataset elettorali su `UPPER(TRIM(comune))` con
  `LEFT JOIN`; la provincia serve solo per i 5 nomi ambigui.
- motivo: le province storiche hanno nomi diversi dallo snapshot SUT
  (`VERBANIA`/`VERB.-CUS.OSSOLA`/`VERBANO-CUSIO-OSSOLA`, `FORLI`/`RIMINI`/…),
  e il match comune+provincia scende da ~91% a ~78%.
- impatto: `codice_istat` può essere NULL; tenere sempre la riga e aggiungere
  un flag di copertura nei clean dei dataset.


