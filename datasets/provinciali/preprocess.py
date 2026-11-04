#!/usr/bin/env python3
"""Scarica e normalizza i TXT delle elezioni provinciali da Eligendo.

Uso: python preprocess.py <anno> <output.csv>
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from _shared.eligendo import download_bytes, read_table, select_entries  # noqa: E402

BASE_URL = "https://dait.interno.gov.it/documenti/opendata/provinciali"

DATES: dict[int, list[str]] = {
    2004: ["20040612"],
    2005: ["20050403", "20050508"],
    2006: ["20060528"],
    2007: ["20070527"],
    2008: ["20080413"],
    2009: ["20090607"],
    2010: ["20100328", "20100530"],
    2011: ["20110515"],
}

NUMERIC_FIELDS = frozenset(
    {
        "turno",
        "elettori",
        "elettori_maschi",
        "votanti",
        "votanti_maschi",
        "schede_bianche",
        "voti_lista",
        "voti_candidato",
    }
)

COL_MAP: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^REG(IONE)?$", re.I), "regione"),
    (re.compile(r"^PROV(INCIA)?$", re.I), "provincia"),
    (re.compile(r"^COLLEGIO$", re.I), "collegio"),
    (re.compile(r"^COMUNE$", re.I), "comune"),
    (re.compile(r"^TURNO$", re.I), "turno"),
    (re.compile(r"^(ELETTORI(TOT)?|ELETTORITOT)$", re.I), "elettori"),
    (re.compile(r"^(ELETTORI_MASCHI|ELETTORIMASCHI|ELETTORI_M)$", re.I), "elettori_maschi"),
    (re.compile(r"^(VOTANTI(TOT)?|VOTANTITOT)$", re.I), "votanti"),
    (re.compile(r"^(VOTANTI_MASCHI|VOTANTIMASCHI|VOTANTI_M)$", re.I), "votanti_maschi"),
    (re.compile(r"^(SCHEDE_BIANCHE|SKBIANCHE|SCHEDEBIANCHE)$", re.I), "schede_bianche"),
    (re.compile(r"^(LISTA|DESCRLISTA)$", re.I), "lista"),
    (re.compile(r"^(VOTI_LISTA|VOTILISTA|TOTVOTI)$", re.I), "voti_lista"),
    (
        re.compile(
            r"^(VOTI_CAND(IDATO)?|VOTICAND(IDATO)?|VOTICANDIDSINDACO|VOTICANDLEADER)$",
            re.I,
        ),
        "voti_candidato",
    ),
    (re.compile(r"^COGNOME$", re.I), "cognome"),
    (re.compile(r"^NOME$", re.I), "nome"),
    (re.compile(r"^DATANASCITA$", re.I), "data_nascita"),
    (re.compile(r"^LUOGONASCITA$", re.I), "luogo_nascita"),
    (re.compile(r"^SESSO$", re.I), "sesso"),
    (re.compile(r"^(CODTIPOELETTO|ELETTO)$", re.I), "cod_tipo_elettore"),
]


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


def normalize_columns(header: list[str]) -> tuple[list[str], list[int]]:
    names: list[str] = []
    indices: list[int] = []
    for i, col in enumerate(header):
        col = col.strip().strip('"')
        for pattern, name in COL_MAP:
            if pattern.match(col):
                names.append(name)
                indices.append(i)
                break
    return names, indices


def records_from_rows(
    header: list[str], rows: list[list[str]], election_date: str
) -> list[dict]:
    names, indices = normalize_columns(header)
    records: list[dict] = []
    for row in rows:
        if not row or not any(cell.strip() for cell in row):
            continue
        rec: dict[str, str] = {"data_elezione": election_date}
        for name, idx in zip(names, indices):
            if idx < len(row):
                val = row[idx].strip().strip('"')
                if name in NUMERIC_FIELDS:
                    val = normalize_number(val)
                rec[name] = val
        if "cognome" in rec and "nome" in rec:
            rec["candidato"] = f"{rec.pop('cognome', '')} {rec.pop('nome', '')}".strip()
        records.append(rec)
    return records


def main() -> None:
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2011
    output = sys.argv[2] if len(sys.argv) > 2 else "raw_input.csv"

    dates = DATES.get(year)
    if not dates:
        print(f"Nessuna fonte configurata per l'anno {year}", file=sys.stderr)
        sys.exit(1)

    all_records: list[dict] = []
    for date in dates:
        election_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
        url = f"{BASE_URL}/provinciali-{date}.zip"
        print(f"  {election_date} -> download...", file=sys.stderr)
        payload = download_bytes(url)
        entries = select_entries(payload, match="*.txt")
        if not entries:
            print(f"    nessun TXT nello ZIP {url}", file=sys.stderr)
            continue
        name, data = next(iter(entries.items()))
        header, rows = read_table(data, name)
        records = records_from_rows(header, rows, election_date)
        print(f"    {len(records)} righe", file=sys.stderr)
        all_records.extend(records)

    if not all_records:
        print("Nessun dato estratto!", file=sys.stderr)
        sys.exit(1)

    fieldnames: list[str] = []
    seen: set[str] = set()
    for rec in all_records:
        for key in rec:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)

    with open(output, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(all_records)

    print(f"Fatto: anno={year} totale={len(all_records)} righe -> {output}", file=sys.stderr)


if __name__ == "__main__":
    main()
