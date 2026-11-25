#!/usr/bin/env python3
"""Scarica e normalizza i CSV delle elezioni regionali da Eligendo.

Uso: python preprocess.py <anno> <output.csv>

Scarica ZIP/CSV da Eligendo per l'anno specificato, estrae il file scrutini,
normalizza colonne e numeri, e produce un CSV unico con schema standard.
"""

import csv
import io
import os
import re
import sys
import urllib.request
import zipfile

# ── mappa anni → lista di (url, data_elezione, is_zip) ──────────────────
SOURCES: dict[int, list[tuple[str, str, bool]]] = {
    1970: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-19700607.zip",
            "1970-06-07",
            True,
        ),
    ],
    1975: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-19750615.zip",
            "1975-06-15",
            True,
        ),
    ],
    1980: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-19800608.zip",
            "1980-06-08",
            True,
        ),
    ],
    1985: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-19850512.zip",
            "1985-05-12",
            True,
        ),
    ],
    1990: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-19900506.zip",
            "1990-05-06",
            True,
        ),
    ],
    1995: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-19950423.zip",
            "1995-04-23",
            True,
        ),
    ],
    2000: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20000416.zip",
            "2000-04-16",
            True,
        ),
    ],
    2001: [
        # 2001-06-24: elezione suppletiva in Sicilia, CSV dentro ZIP.
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20010624.zip",
            "2001-06-24",
            True,
        ),
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20011111.zip",
            "2001-11-11",
            True,
        ),
    ],
    2005: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20050403.zip",
            "2005-04-03",
            True,
        ),
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20050417.zip",
            "2005-04-17",
            True,
        ),
    ],
    2006: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20061105.zip",
            "2006-11-05",
            True,
        ),
    ],
    2008: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20081214.zip",
            "2008-12-14",
            True,
        ),
    ],
    2010: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20100328.zip",
            "2010-03-28",
            True,
        ),
    ],
    # 2011-10-16 escluso: la fonte pubblica solo XLSX.
    2013: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20130224.zip",
            "2013-02-24",
            True,
        ),
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20131117.zip",
            "2013-11-17",
            True,
        ),
    ],
    2014: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20140525.zip",
            "2014-05-25",
            True,
        ),
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20141123.zip",
            "2014-11-23",
            True,
        ),
    ],
    2015: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20150531.zip",
            "2015-05-31",
            True,
        ),
    ],
    2018: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20180304.zip",
            "2018-03-04",
            True,
        ),
    ],
    2019: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20190210.zip",
            "2019-02-10",
            True,
        ),
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20190324.zip",
            "2019-03-24",
            True,
        ),
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20190526.zip",
            "2019-05-26",
            True,
        ),
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20191027.zip",
            "2019-10-27",
            True,
        ),
    ],
    2020: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20200126.zip",
            "2020-01-26",
            True,
        ),
        # 2020-09-20 escluso: file XLSX non gestiti
    ],
    2021: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20211003.zip",
            "2021-10-03",
            True,
        ),
    ],
    2023: [
        (
            "https://dait.interno.gov.it/documenti/opendata/catalogoagid/regionali-20230212.csv",
            "2023-02-12",
            False,
        ),
    ],
    2024: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20240310.zip",
            "2024-03-10",
            True,
        ),
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20240421.zip",
            "2024-04-21",
            True,
        ),
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20240609.zip",
            "2024-06-09",
            True,
        ),
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20241027.zip",
            "2024-10-27",
            True,
        ),
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20241117.zip",
            "2024-11-17",
            True,
        ),
    ],
    2025: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20251005.zip",
            "2025-10-05",
            True,
        ),
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20251012.zip",
            "2025-10-12",
            True,
        ),
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20251123.zip",
            "2025-11-23",
            True,
        ),
    ],
}


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def normalize_number(val: str) -> str:
    """Normalizza numero: rimuovi punti migliaia, trasforma virgola in punto.
    Esempi: '1.234,56' → '1234.56', '5849,00' → '5849', '1234' → '1234'"""
    val = val.strip().strip('"')
    if not val or val in ("***", "-"):
        return ""
    if "," in val:
        val = val.replace(".", "").replace(",", ".")
        # Se era intero con virgola (.00), rimuovi la parte decimale
        if val.endswith(".0"):
            val = val[:-2]
    else:
        val = val.replace(".", "")
    return val


def smart_decode(data: bytes) -> str:
    """Decode bytes tentando UTF-8 prima, poi latin-1/ISO-8859-1."""
    for enc in ("utf-8-sig", "utf-8", "iso-8859-1", "cp1252"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def _to_int(value) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(float(str(value).replace(",", ".")))
    except (TypeError, ValueError):
        return None


def _parse_entries(raw: bytes, is_zip: bool, url: str) -> list[tuple[str, list[list[str]]]]:
    """Entry tabellari dello ZIP (o il file singolo), con nome e righe."""
    if not is_zip:
        return [(os.path.basename(url), parse_csv(smart_decode(raw)))]
    entries: list[tuple[str, list[list[str]]]] = []
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        for name in zf.namelist():
            base = os.path.basename(name)
            if not base or base.startswith("~") or base.startswith("."):
                continue
            if not base.lower().endswith((".csv", ".txt")):
                continue
            rows = parse_csv(smart_decode(zf.read(name)))
            if rows:
                entries.append((base, rows))
    return entries


def _records_from_rows(rows: list[list[str]], election_date: str) -> list[dict]:
    header = rows[0]
    col_names, col_indices = normalize_columns(header)
    records = []
    for row in rows[1:]:
        if not row or not any(cell.strip() for cell in row):
            continue
        rec = {"data_elezione": election_date}
        for name, idx in zip(col_names, col_indices):
            if idx < len(row):
                val = row[idx].strip().strip('"')
                if name in (
                    "elettori",
                    "votanti",
                    "schede_bianche",
                    "voti_lista",
                    "voti_candidato",
                ):
                    val = normalize_number(val)
                rec[name] = val
        if "cognome" in rec and "nome" in rec:
            rec["candidato"] = f"{rec.pop('cognome', '')} {rec.pop('nome', '')}".strip()
        records.append(rec)
    return records


def _aggregate_to_comune(records: list[dict]) -> list[dict]:
    """Se il file e' per sezione, somma i voti per comune e deduplica l'affluenza.

    L'affluenza e' ripetuta su ogni riga candidato della sezione: va presa una
    volta per sezione e poi sommata sui comuni.
    """
    if not any(rec.get("sezione") for rec in records):
        return records

    turnout: dict[tuple[str, str, str, str], dict[str, int | None]] = {}
    for rec in records:
        key = (
            rec.get("regione", ""),
            rec.get("provincia", ""),
            rec.get("comune", ""),
            rec.get("sezione", ""),
        )
        if key in turnout:
            continue
        values = {field: _to_int(rec.get(field)) for field in ("elettori", "votanti", "schede_bianche")}
        if values["elettori"] is not None:
            turnout[key] = values

    per_comune: dict[tuple[str, str, str], dict[str, int]] = {}
    for (regione, provincia, comune, _sezione), values in turnout.items():
        acc = per_comune.setdefault(
            (regione, provincia, comune), {"elettori": 0, "votanti": 0, "schede_bianche": 0}
        )
        for field, value in values.items():
            if value:
                acc[field] += value

    groups: dict[tuple, dict] = {}
    for rec in records:
        key = (
            rec.get("regione", ""),
            rec.get("circoscrizione", ""),
            rec.get("provincia", ""),
            rec.get("comune", ""),
            rec.get("lista", ""),
            rec.get("candidato", ""),
        )
        group = groups.get(key)
        if group is None:
            group = {
                field: rec.get(field, "")
                for field in ("data_elezione", "regione", "circoscrizione", "provincia", "comune", "lista", "candidato")
            }
            group["voti_lista"] = 0
            group["voti_candidato"] = 0
            groups[key] = group
        for field in ("voti_lista", "voti_candidato"):
            value = _to_int(rec.get(field))
            if value is not None:
                group[field] += value

    out: list[dict] = []
    for group in groups.values():
        turnout_comune = per_comune.get(
            (group["regione"], group["provincia"], group["comune"])
        )
        if turnout_comune:
            for field, value in turnout_comune.items():
                if value:
                    group[field] = str(value)
        group["voti_lista"] = str(group["voti_lista"]) if group["voti_lista"] else ""
        group["voti_candidato"] = str(group["voti_candidato"]) if group["voti_candidato"] else ""
        out.append(group)
    return out


def parse_csv(content: str) -> list[list[str]]:
    reader = csv.reader(io.StringIO(content), delimiter=";")
    return [row for row in reader if any(cell.strip() for cell in row)]


# ── Mappa normalizzazione colonne ───────────────────────────────────────
# (pattern nel nome colonna → nome normalizzato)
# Colonne attese da clean.sql: garantite anche per le tornate storiche che non
# le portano (es. 1970-1990 senza candidato/circoscrizione).
CANONICAL_COLS = [
    "data_elezione",
    "regione",
    "circoscrizione",
    "provincia",
    "comune",
    "elettori",
    "votanti",
    "schede_bianche",
    "candidato",
    "voti_candidato",
    "lista",
    "voti_lista",
]

COL_MAP: list[tuple[re.Pattern, str]] = [
    (re.compile(r"^REG(IONE)?$", re.I), "regione"),
    (re.compile(r"^CIRC(OSCR(IZIONE)?)?$", re.I), "circoscrizione"),
    (re.compile(r"^PROV(INCIA)?$", re.I), "provincia"),
    (re.compile(r"^COMUNE$", re.I), "comune"),
    (re.compile(r"^(ELETTORI(TOT)?|ELETTORI_TOTALI|NUMELETTORI)$", re.I), "elettori"),
    (re.compile(r"^(VOTANTI(TOT)?|VOTANTI_TOTALI|NUMVOTANTI)$", re.I), "votanti"),
    (re.compile(r"^SEZIONE$", re.I), "sezione"),
    (re.compile(r"^(SCHEDE_BIANCHE|SKBIANCHE)$", re.I), "schede_bianche"),
    (re.compile(r"^(COGNOME|COGNOME_CANDIDATO)$", re.I), "cognome"),
    (re.compile(r"^(NOME|NOME_CANDIDATO)$", re.I), "nome"),
    (re.compile(r"^(LISTA|DESCRLISTA)$", re.I), "lista"),
    (re.compile(r"^(VOTI_LISTA|VOTILISTA)$", re.I), "voti_lista"),
    (re.compile(r"^(VOTI_CAND(IDATO)?|VOTICAND(IDATO)?|VOTICANDIDLEADER)$", re.I), "voti_candidato"),
]


def normalize_columns(header: list[str]) -> tuple[list[str], list[int]]:
    """Mappa le colonne raw ai nomi standard.
    Restituisce (nomi_normalizzati, indici_validi)."""
    norm = []
    indices = []
    for i, col in enumerate(header):
        col = col.strip().strip('"')
        mapped = None
        for pattern, name in COL_MAP:
            if pattern.match(col):
                mapped = name
                break
        if mapped:
            norm.append(mapped)
            indices.append(i)
    return norm, indices


def process_url(url: str, election_date: str, is_zip: bool) -> list[dict]:
    """Scarica e normalizza una tornata Eligendo. Restituisce lista di dict.

    Gli ZIP dal 2024 possono contenere piu' file: si usano le entry con i voti
    (aggregando a comune quelle per sezione, escludendo le preferenze) e si
    recupera l'affluenza da un'eventuale entry scrutini separata.
    """
    raw = download(url)
    votes: list[dict] = []
    turnout: list[dict] = []
    votes_entries: list[tuple[str, list[dict]]] = []
    turnout_entries: list[tuple[str, list[dict]]] = []

    for name, rows in _parse_entries(raw, is_zip, url):
        if "preferenz" in name.lower():
            continue
        records = _records_from_rows(rows, election_date)
        if not records:
            continue
        if any(rec.get("voti_lista") or rec.get("voti_candidato") for rec in records):
            votes_entries.append((name, records))
        elif any(rec.get("elettori") for rec in records):
            turnout_entries.append((name, records))

    # Un solo ruolo per tornata: se c'e' uno scrutini con voti si usa quello
    # (esclude i file candidati, che ripetono gli stessi voti); a parita',
    # preferisce la granularita' comunale a quella per sezione.
    scrutini = [(name, recs) for name, recs in votes_entries if "scrutini" in name.lower()]
    pool = scrutini or votes_entries
    if scrutini:
        comune_level = [
            (name, recs)
            for name, recs in scrutini
            if not any(rec.get("sezione") for rec in recs)
        ]
        if comune_level:
            pool = comune_level

    for _name, records in pool:
        votes.extend(_aggregate_to_comune(records))
    for _name, records in turnout_entries:
        turnout.extend(records)

    if not votes:
        return []

    if turnout and any(not rec.get("elettori") for rec in votes):
        lookup = {
            (rec.get("regione", ""), rec.get("provincia", ""), rec.get("comune", "")): rec
            for rec in turnout
        }
        for rec in votes:
            if rec.get("elettori"):
                continue
            match = lookup.get(
                (rec.get("regione", ""), rec.get("provincia", ""), rec.get("comune", ""))
            )
            if match:
                for field in ("elettori", "votanti", "schede_bianche"):
                    if match.get(field):
                        rec[field] = match[field]

    return votes


def ensure_canonical(records: list[dict]) -> None:
    """Garantisce le colonne attese da clean.sql su ogni record."""
    for rec in records:
        for col in CANONICAL_COLS:
            rec.setdefault(col, "")


def main():
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2023
    output = sys.argv[2] if len(sys.argv) > 2 else "raw_input.csv"

    sources = SOURCES.get(year)
    if not sources:
        print(f"Nessuna fonte configurata per l'anno {year}", file=sys.stderr)
        sys.exit(1)

    all_records: list[dict] = []
    for url, election_date, is_zip in sources:
        print(f"  {election_date} → download...", file=sys.stderr)
        records = process_url(url, election_date, is_zip)
        print(f"    {len(records)} righe", file=sys.stderr)
        all_records.extend(records)

    if not all_records:
        print("Nessun dato estratto!", file=sys.stderr)
        sys.exit(1)

    ensure_canonical(all_records)

    # Ricava header dall'unione delle chiavi di tutti i record
    fieldnames: list[str] = []
    seen: set[str] = set()
    for rec in all_records:
        for key in rec:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(all_records)

    print(f"✅ Fatto: anno={year} totale={len(all_records)} righe → {output}", file=sys.stderr)


if __name__ == "__main__":
    main()
