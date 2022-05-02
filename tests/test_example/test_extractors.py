from contextlib import contextmanager
from pathlib import Path

import fiona

from geocoding.extractors.gadm36 import CountriesExtractor


def test_gadm_countries_extractor(load_json, monkeypatch):
    gadm_row = load_json('gadm36_0_row.json')

    @contextmanager
    def get_rows(*args, **kwargs):
        yield [gadm_row] * 5

    monkeypatch.setattr(fiona, "open", get_rows)

    extractor = CountriesExtractor(Path('dummy_path'))

    assert list(extractor) == [('Aruba', 'ABW')] * 5
