#!/usr/bin/env python3
"""Scarica e normalizza i CSV dei referendum da Eligendo.

Uso: python preprocess.py <anno> <output.csv>
"""

import csv
import io
import os
import re
import sys
import zipfile

from lab_connectors.http.download import download as _lab_download

SOURCES: dict[int, list[tuple[str, str, bool]]] = {
    1974: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-19740512.zip",
            "1974-05-12",
            True,
        )
    ],
    1978: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-19780611.zip",
            "1978-06-11",
            True,
        )
    ],
    1981: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-19810517.zip",
            "1981-05-17",
            True,
        )
    ],
    1985: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-19850609.zip",
            "1985-06-09",
            True,
        )
    ],
    1987: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-19871108.zip",
            "1987-11-08",
            True,
        )
    ],
    1989: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-19890618.zip",
            "1989-06-18",
            True,
        )
    ],
    1990: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-19900603.zip",
            "1990-06-03",
            True,
        )
    ],
    1991: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-19910609.zip",
            "1991-06-09",
            True,
        )
    ],
    1993: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-19930418.zip",
            "1993-04-18",
            True,
        )
    ],
    1995: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-19950611.zip",
            "1995-06-11",
            True,
        )
    ],
    1997: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-19970615.zip",
            "1997-06-15",
            True,
        )
    ],
    1999: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-19990418.zip",
            "1999-04-18",
            True,
        )
    ],
    2000: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20000521.zip",
            "2000-05-21",
            True,
        )
    ],
    2001: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20011007.zip",
            "2001-10-07",
            True,
        )
    ],
    2003: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20030615.zip",
            "2003-06-15",
            True,
        )
    ],
    2005: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20050612.zip",
            "2005-06-12",
            True,
        )
    ],
    2006: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20060625.zip",
            "2006-06-25",
            True,
        )
    ],
    2009: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20090621.zip",
            "2009-06-21",
            True,
        )
    ],
    2011: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20110612.zip",
            "2011-06-12",
            True,
        )
    ],
    2016: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20160417.zip",
            "2016-04-17",
            True,
        ),
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20161204.zip",
            "2016-12-04",
            True,
        ),
    ],
    2020: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20200920.zip",
            "2020-09-20",
            True,
        )
    ],
    2022: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20220612.zip",
            "2022-06-12",
            True,
        )
    ],
    2025: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20250608.zip",
            "2025-06-08",
            True,
        )
    ],
    2026: [
        (
            "https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20260322.zip",
            "2026-03-22",
            True,
        )
    ],
}

# Alcuni ZIP storici (es. 1985) non hanno la riga di intestazione: le colonne
# sono in ordine fisso. Usato solo quando la prima riga non ha nomi riconoscibili.
HEADERLESS_COLS = [
    "REGIONE",
    "PROVINCIA",
    "COMUNE",
    "NUM_REFERENDUM",
    "QUESITO",
    "ELETTORI",
    "ELETTORI_MASCHI",
    "VOTANTI",
    "VOTANTI_MASCHI",
    "NUMVOTISI",
    "NUMVOTINO",
    "SCHEDE_BIANCHE",
]

COL_MAP: list[tuple[re.Pattern, str]] = [
    (re.compile(r"^REGIONE$", re.I), "regione"),
    (re.compile(r"^REG$", re.I), "regione"),
    (re.compile(r"^PROV(INCIA)?$", re.I), "provincia"),
    (re.compile(r"^COM$", re.I), "comune"),
    (re.compile(r"^COMUNE$", re.I), "comune"),
    (re.compile(r"^SEZIONE$", re.I), "sezione"),
    (
        re.compile(r"^(ELETTORI_UOMINI|ELETTORI_MASCHI|ELETTORIMASCHI|ELETTORI MASCHI)$", re.I),
        "elettori_uomini",
    ),
    (re.compile(r"^(ELETTORI(TOT)?|ELETTORITOTALI)$", re.I), "elettori"),
    (
        re.compile(r"^(VOTANTI_UOMINI|VOTANTI_MASCHI|VOTANTIMASCHI|VOTANTI MASCHI)$", re.I),
        "votanti_uomini",
    ),
    (re.compile(r"^(VOTANTI(TOT)?|NUMVOTANTITOTALI)$", re.I), "votanti"),
    (re.compile(r"^(VOTI_SI|VOTISI|NUMVOTISI)$", re.I), "voti_si"),
    (re.compile(r"^(VOTI_NO|VOTINO|NUMVOTINO)$", re.I), "voti_no"),
    (re.compile(r"^(SCHEDE_NULLE|SCHEDENULLE)$", re.I), "schede_nulle"),
    (re.compile(r"^(SCHEDE_BIANCHE|SKBIANCHE|SCHEDEBIANCHE)$", re.I), "schede_bianche"),
    (re.compile(r"^(SCHEDE_CONTESTATE|SCHEDECONTESTATE)$", re.I), "schede_contestate"),
    (re.compile(r"^(NUM_REFERENDUM|NUMREFERENDUM|N_QUESITO|NUMQUESITO)$", re.I), "num_quesito"),
    (re.compile(r"^(QUESITO|DESCR_REFERENDUM|QUESITOREFERENDUM)$", re.I), "descrizione_quesito"),
    (re.compile(r"^VOTIVALIDI_SI$", re.I), "voti_si"),
    (re.compile(r"^VOTIVALIDI$", re.I), "voti_validi"),
]


def download(url: str) -> bytes:
    return _lab_download(url, timeout=120)


def normalize_number(val: str) -> str:
    val = val.strip().strip('"')
    if not val or val in ("***", "-", "N.D."):
        return ""
    if "," in val:
        val = val.replace(".", "").replace(",", ".")
        if val.endswith(".0"):
            val = val[:-2]
    else:
        val = val.replace(".", "")
    return val


def smart_decode(data: bytes) -> str:
    for enc in ("utf-8-sig", "utf-8", "iso-8859-1", "cp1252"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def parse_csv(content: str) -> list[list[str]]:
    first_line = next((line for line in content.splitlines() if line.strip()), "")
    delimiter = "\t" if first_line.count("\t") > first_line.count(";") else ";"
    reader = csv.reader(io.StringIO(content, newline=""), delimiter=delimiter)
    return [row for row in reader if any(cell.strip() for cell in row)]


def normalize_columns(header: list[str]) -> tuple[list[str], list[int]]:
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


def _num(value) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(float(str(value).replace(",", ".")))
    except (TypeError, ValueError):
        return None


def _pick_header(rows: list[list[str]]) -> tuple[int | None, list[str], list[int]]:
    """Trova la riga di intestazione (alcuni file hanno un titolo davanti)."""
    for index, row in enumerate(rows[:6]):
        names, indices = normalize_columns(row)
        if len(names) >= 3:
            return index, names, indices
    return None, [], []


def parse_zip_bytes(raw: bytes, election_date: str) -> list[dict]:
    entries: list[tuple[str, list[list[str]]]] = []
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        for name in zf.namelist():
            base = os.path.basename(name)
            if not base or base.startswith("~") or base.startswith("."):
                continue
            if not base.lower().endswith((".csv", ".txt")):
                continue
            if "votanti" in base.lower():
                continue
            rows = parse_csv(smart_decode(zf.read(name)))
            if rows:
                entries.append((base, rows))

    # LivComune vince sulle varianti per sezione; i file estero restano fuori
    # quando esiste la copertura Italia.
    selected = [entry for entry in entries if "livcomune" in entry[0].lower()]
    if not selected:
        selected = [entry for entry in entries if "estero" not in entry[0].lower()]
    if not selected:
        selected = entries
    if selected and all(
        "livsez" in name.lower() or "_sez" in name.lower() for name, _ in selected
    ):
        raise ValueError(
            "Referendum: fonte solo per sezione (LivSez) senza LivComune; "
            "l'aggregazione a comune non e' implementata"
        )

    records: list[dict] = []
    for _base, rows in selected:
        header_index, col_names, col_indices = _pick_header(rows)
        title = ""
        if header_index is None:
            # Fonte senza intestazione (es. 1985): la prima riga e' gia' un record.
            col_names, col_indices = normalize_columns(HEADERLESS_COLS)
            data_rows = rows
        else:
            if header_index > 0:
                title = " ".join(cell.strip() for cell in rows[0] if cell.strip())
            data_rows = rows[header_index + 1:]

        for row in data_rows:
            if not row or not any(cell.strip() for cell in row):
                continue
            rec = {"data_elezione": election_date}
            for cname, idx in zip(col_names, col_indices):
                if idx < len(row):
                    val = row[idx].strip().strip('"')
                    if cname in (
                        "elettori",
                        "elettori_uomini",
                        "votanti",
                        "votanti_uomini",
                        "voti_si",
                        "voti_no",
                        "voti_validi",
                        "schede_nulle",
                        "schede_bianche",
                        "schede_contestate",
                        "num_quesito",
                    ):
                        val = normalize_number(val)
                    rec[cname] = val
            if not rec.get("voti_no"):
                validi, si = _num(rec.get("voti_validi")), _num(rec.get("voti_si"))
                if validi is not None and si is not None:
                    rec["voti_no"] = str(validi - si)
            if title and not rec.get("descrizione_quesito"):
                rec["descrizione_quesito"] = title
            records.append(rec)

    if records and not any(rec.get("num_quesito") for rec in records):
        for rec in records:
            rec["num_quesito"] = "1"
    return records


def process_zip(url: str, election_date: str) -> list[dict]:
    return parse_zip_bytes(download(url), election_date)


def main():
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2022
    output = sys.argv[2] if len(sys.argv) > 2 else "raw_input.csv"

    sources = SOURCES.get(year)
    if not sources:
        print(f"Nessuna fonte configurata per l'anno {year}", file=sys.stderr)
        sys.exit(1)

    all_records: list[dict] = []
    for url, election_date, is_zip in sources:
        print(f"  {election_date} -> download...", file=sys.stderr)
        records = process_zip(url, election_date)
        print(f"    {len(records)} righe", file=sys.stderr)
        all_records.extend(records)

    if not all_records:
        print("Nessun dato estratto!", file=sys.stderr)
        sys.exit(1)

    canonical_cols = [
        "data_elezione",
        "data_elezione_raw",
        "tipo_elezione",
        "regione",
        "provincia",
        "comune",
        "sezione",
        "num_quesito",
        "descrizione_quesito",
        "elettori",
        "elettori_uomini",
        "votanti",
        "votanti_uomini",
        "voti_si",
        "voti_no",
        "schede_nulle",
        "schede_bianche",
        "schede_contestate",
    ]
    for rec in all_records:
        for col in canonical_cols:
            rec.setdefault(col, "")

    seen = set()
    for rec in all_records:
        for k in rec:
            seen.add(k)
    fieldnames = sorted(seen)

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(all_records)

    print(f"Fatto: anno={year} totale={len(all_records)} righe -> {output}", file=sys.stderr)


if __name__ == "__main__":
    main()
