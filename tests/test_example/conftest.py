import json

import pytest
from pathlib import Path

STATIC_DIR = Path(__file__).parent.resolve() / 'static'


@pytest.fixture
def load_json():
    def _load_json(path: str):
        with (STATIC_DIR / path).open('r') as f:
            return json.load(f)
    return _load_json
