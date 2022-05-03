from contextlib import contextmanager
from pathlib import Path

import fiona
import pytest

from geocoding.extractors.gadm36 import CountriesExtractor, CountryGADM


@pytest.fixture
def gadm_row(load_json):
    return load_json("gadm36_0_row.json")


def test_gadm_country_model(gadm_row):
    country = CountryGADM.from_shapefile_object(gadm_row)
    assert country.id == 0
    assert country.name == "Aruba"
    assert country.code == "ABW"
    assert len(country.geometry) == 1
    assert len(country.geometry[0]["coordinates"][0]) == 2161


def test_gadm_countries_extractor(gadm_row, monkeypatch):
    @contextmanager
    def get_rows(*args, **kwargs):
        yield [gadm_row] * 5

    monkeypatch.setattr(fiona, "open", get_rows)

    extractor = CountriesExtractor(Path("dummy_path"))
    countries = list(extractor)

    assert all(map(lambda country: country.id == 0, countries))
    assert all(map(lambda country: country.name == "Aruba", countries))
    assert all(map(lambda country: country.code == "ABW", countries))
