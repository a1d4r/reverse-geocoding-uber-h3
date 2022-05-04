from geocoding.models.gadm import GADMCountry, GADMCountrySubdivision


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
    assert subdivision.hasc_code == "AF.BG"
    assert len(subdivision.geometry) == 1
    assert len(subdivision.geometry[0]["coordinates"][0]) == 647
