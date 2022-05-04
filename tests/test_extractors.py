from contextlib import contextmanager
from pathlib import Path

import fiona

from geocoding.extractors.gadm import (
    GADMCountriesExtractor,
    GADMCountrySubdivisionsExtractor,
)


def test_gadm_countries_extractor(gadm_country_row, monkeypatch):
    @contextmanager
    def get_rows(*args, **kwargs):
        yield [gadm_country_row] * 5

    monkeypatch.setattr(fiona, "open", get_rows)

    extractor = GADMCountriesExtractor(Path("dummy_path"))
    countries = list(extractor)

    assert all(map(lambda country: country.id == 0, countries))
    assert all(map(lambda country: country.name == "Aruba", countries))
    assert all(map(lambda country: country.code == "ABW", countries))


def test_gadm_country_subdivisions_extractor(gadm_country_subdivision_row, monkeypatch):
    @contextmanager
    def get_rows(*args, **kwargs):
        yield [gadm_country_subdivision_row] * 5

    monkeypatch.setattr(fiona, "open", get_rows)

    extractor = GADMCountrySubdivisionsExtractor(Path("dummy_path"))
    subdivisions = list(extractor)

    assert all(map(lambda country: country.id == 1, subdivisions))
    assert all(map(lambda country: country.name == "Badghis", subdivisions))
    assert all(map(lambda country: country.code == "AFG.2_1", subdivisions))
