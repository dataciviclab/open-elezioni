#!/usr/bin/env python3
"""Costruisce il bridge comuni SUT: codici + regione/provincia.

Fonte: SUT open data (DAIT).
- elenco-codici-comuni: comune, sigla, codice elettorale, ISTAT, Belfiore
- elenco-sezioni: regione, provincia, comune, COD. ISTAT (per il nome di
  regione/provincia, che i codici non portano)

Il file sezioni ha una riga di titolo e i codici in formato Excel `="069001"`:
va ripulito prima del parsing.
"""

from __future__ import annotations

import csv
import io
import sys

from lab_connectors.http.download import download as _download

BASE = "https://dait.interno.gov.it/territorio-e-autonomie-locali/indice-sut/open-data"
CODICI_URL = f"{BASE}/elenco-codici-comuni-csv.php"
SEZIONI_URL = f"{BASE}/elenco-sezioni-csv.php"


def _text(url: str) -> str:
    return _download(url, timeout=180).decode("utf-8-sig", errors="replace")


def _strip_excel_codes(text: str) -> str:
    # `="069001"` -> `069001`
    return text.replace('="', "").replace('"', "")


def _geo_by_istat(sezioni_text: str) -> dict[str, tuple[str, str]]:
    rows = [
        row
        for row in csv.reader(io.StringIO(_strip_excel_codes(sezioni_text)), delimiter=";")
        if any(cell.strip() for cell in row)
    ]
    # riga 0 = titolo, riga 1 = header
    geo: dict[str, tuple[str, str]] = {}
    for row in rows[2:]:
        if len(row) < 4:
            continue
        istat = row[3].strip()
        if istat:
            geo.setdefault(istat, (row[0].strip(), row[1].strip()))
    return geo


def main() -> None:
    output = sys.argv[1] if len(sys.argv) > 1 else "raw_input.csv"

    codici = list(csv.DictReader(io.StringIO(_text(CODICI_URL)), delimiter=";"))
    geo = _geo_by_istat(_text(SEZIONI_URL))

    records: list[dict[str, str]] = []
    for row in codici:
        comune = (row.get("DESCRIZIONE COMUNE") or "").strip()
        istat = (row.get("CODICE ISTAT") or "").strip().replace('="', "").replace('"', "")
        if not comune or not istat:
            continue
        regione, provincia = geo.get(istat, ("", ""))
        records.append(
            {
                "comune": comune,
                "sigla": (row.get("SIGLA") or "").strip(),
                "regione": regione,
                "provincia": provincia,
                "codice_istat": istat,
                "codice_belfiore": (row.get("CODICE BELFIORE") or "").strip(),
                "codice_elettorale": (row.get("CODICE ELETTORALE") or "").strip(),
            }
        )

    fieldnames = [
        "comune",
        "sigla",
        "regione",
        "provincia",
        "codice_istat",
        "codice_belfiore",
        "codice_elettorale",
    ]
    with open(output, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(records)

    print(f"bridge: {len(records)} comuni -> {output}", file=sys.stderr)


if __name__ == "__main__":
    main()
