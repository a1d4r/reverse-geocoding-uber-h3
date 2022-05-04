import json
from pathlib import Path

import pytest

STATIC_DIR = Path(__file__).parent.resolve() / "static"


@pytest.fixture
def load_json():
    def _load_json(path: str):
        with (STATIC_DIR / path).open("r") as f:
            return json.load(f)

    return _load_json


@pytest.fixture
def gadm_country_row(load_json):
    return load_json("gadm36_0_row.json")


@pytest.fixture
def gadm_country_subdivision_row(load_json):
    return load_json("gadm36_1_row.json")
