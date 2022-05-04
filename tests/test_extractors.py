from contextlib import contextmanager
from pathlib import Path

import fiona
import pytest

from geocoding.extractors.gadm36 import (
    GADMCountriesExtractor,
    GADMCountry,
    GADMCountrySubdivision,
    GADMCountrySubdivisionsExtractor,
)


@pytest.fixture
def gadm_country_row(load_json):
    return load_json("gadm36_0_row.json")


@pytest.fixture
def gadm_country_subdivision_row(load_json):
    return load_json("gadm36_1_row.json")


def test_gadm_country_model(gadm_country_row):
    country = GADMCountry.from_shapefile_object(gadm_country_row)
    assert country.id == 0
    assert country.name == "Aruba"
    assert country.code == "ABW"
    assert len(country.geometry) == 1
    assert len(country.geometry[0]["coordinates"][0]) == 2161


def test_gadm_country_subdivision_model(gadm_country_subdivision_row):
    subdivision = GADMCountrySubdivision.from_shapefile_object(
        gadm_country_subdivision_row
    )
    assert subdivision.id == 1
    assert subdivision.name == "Badghis"
    assert subdivision.code == "AFG.2_1"
    assert subdivision.other_names == ["Badghes", "Badghisat", "Badgis"]
    assert subdivision.localized_names == []
    assert subdivision.administrative_type == "Province"
    assert subdivision.localized_administrative_type == "Velayat"
    assert subdivision.country_code == "AFG"
    assert subdivision.country_name == "Afghanistan"
    assert len(subdivision.geometry) == 1
    assert len(subdivision.geometry[0]["coordinates"][0]) == 647


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
