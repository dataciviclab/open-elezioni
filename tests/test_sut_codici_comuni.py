"""Contract test per il support dataset SUT codici comuni.

Verifica che `clean.sql` trasformi davvero il formato Excel `="028001"` nel
codice ISTAT `028001`. Marker: contract.
"""

from __future__ import annotations

from pathlib import Path

import duckdb
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
DATASET = REPO_ROOT / "support" / "sut-codici-comuni"

SAMPLE = (
    "NR.;DESCRIZIONE COMUNE;SIGLA;CODICE ELETTORALE;CODICE ISTAT;CODICE BELFIORE\n"
    '1;ABANO TERME;PD;1050540010;="028001";A001\n'
)


@pytest.mark.contract
def test_clean_estrae_codice_istat(tmp_path: Path) -> None:
    csv_path = tmp_path / "sut.csv"
    csv_path.write_text(SAMPLE, encoding="utf-8")
    sql = (DATASET / "sql" / "clean.sql").read_text(encoding="utf-8")

    con = duckdb.connect()
    con.execute("CREATE MACRO normalize_string(x) AS trim(upper(x))")
    con.execute(
        "CREATE TABLE raw_input AS "
        f"SELECT * FROM read_csv('{csv_path}', delim=';', header=true, all_varchar=true)"
    )
    row = con.execute(sql).fetchone()

    assert row is not None
    assert row[1] == "ABANO TERME"
    assert row[2] == "PD"
    assert row[4] == "028001"
    assert row[5] == "A001"


@pytest.mark.contract
def test_dataset_config_ha_le_chiavi_attese() -> None:
    import yaml

    cfg = yaml.safe_load((DATASET / "dataset.yml").read_text(encoding="utf-8"))

    assert cfg["dataset"]["source_id"] == "dait_sut"
    assert cfg["clean"]["required_columns"] == [
        "nr",
        "comune",
        "sigla",
        "codice_elettorale",
        "codice_istat",
        "codice_belfiore",
    ]
