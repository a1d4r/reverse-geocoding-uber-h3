from typing import Optional

from geocoding import settings
from geocoding.convertors.h3 import get_hexagon_by_point
from geocoding.models.cql import HexCountry, HexCountrySubdivision
from geocoding.scylla.connector import ScyllaConnector
from geocoding.scylla.session import get_session
from geocoding.storage import CountriesStorage, CountrySubdivisionsStorage

session = get_session(settings.SCYLLA_KEYSPACE)
scylla = ScyllaConnector(session)
countries_storage = CountriesStorage(scylla)
subdivisions_storage = CountrySubdivisionsStorage(scylla)


def get_country_by_point(lat: float, lng: float) -> Optional[HexCountry]:
    hex_id = get_hexagon_by_point(lat, lng, settings.COUNTRIES_H3_RESOLUTION)
    return countries_storage.read(hex_id)


def get_get_country_subdivision_by_point(
    lat: float, lng: float
) -> Optional[HexCountrySubdivision]:
    hex_id = get_hexagon_by_point(lat, lng, settings.SUBDIVISIONS_H3_RESOLUTION)
    return subdivisions_storage.read(hex_id)
