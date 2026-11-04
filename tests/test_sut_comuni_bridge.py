"""Contract test per il preprocess del bridge SUT.

Verifica il parsing del file sezioni: riga di titolo, codici Excel `="069001"`,
dedup per ISTAT. Marker: contract.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "support" / "sut-comuni-bridge" / "preprocess.py"

SEZIONI = (
    " ELENCO SEZIONI  ITALIA (dati aggiornati dai comuni)\n"
    'REGIONE;PROVINCIA;COMUNE;COD. ISTAT;N. SEZIONE\n'
    'VENETO;PADOVA;ABANO TERME;="028001";1\n'
    'VENETO;PADOVA;ABANO TERME;="028001";2\n'
    "LOMBARDIA;LODI;ABBADIA CERRETO;=\"098001\";1\n"
)


def _load_module():
    spec = importlib.util.spec_from_file_location("sut_bridge_preprocess", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_strip_excel_codes():
    module = _load_module()
    assert module._strip_excel_codes('="069001"') == "069001"


def test_geo_by_istat_salta_titolo_e_deduplica():
    module = _load_module()

    geo = module._geo_by_istat(SEZIONI)

    assert geo == {
        "028001": ("VENETO", "PADOVA"),
        "098001": ("LOMBARDIA", "LODI"),
    }
