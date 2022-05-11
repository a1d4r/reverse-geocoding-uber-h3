from typing import NamedTuple, Optional

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


class Coordinates(NamedTuple):
    lat: float
    lon: float


def get_country_by_point(lat: float, lng: float) -> Optional[HexCountry]:
    hex_id = get_hexagon_by_point(lat, lng, settings.COUNTRIES_H3_RESOLUTION)
    return countries_storage.read(hex_id)


def get_countries_by_points(
    points: list[Coordinates],
) -> dict[Coordinates, Optional[HexCountry]]:
    hex_id_by_coords = {
        coords: get_hexagon_by_point(*coords, settings.COUNTRIES_H3_RESOLUTION)
        for coords in points
    }
    countries_by_hex_id = countries_storage.read_many(list(hex_id_by_coords.values()))
    return {
        coords: countries_by_hex_id[hex_id]
        for coords, hex_id in hex_id_by_coords.items()
    }


def get_country_subdivision_by_point(
    lat: float, lng: float
) -> Optional[HexCountrySubdivision]:
    hex_id = get_hexagon_by_point(lat, lng, settings.SUBDIVISIONS_H3_RESOLUTION)
    return subdivisions_storage.read(hex_id)


def get_countries_subdivisions_by_points(
    points: list[Coordinates],
) -> dict[Coordinates, Optional[HexCountrySubdivision]]:
    hex_id_by_coords = {
        coords: get_hexagon_by_point(*coords, settings.COUNTRIES_H3_RESOLUTION)
        for coords in points
    }
    subdivisions_by_hex_id = subdivisions_storage.read_many(
        list(hex_id_by_coords.values())
    )
    return {
        coords: subdivisions_by_hex_id[hex_id]
        for coords, hex_id in hex_id_by_coords.items()
    }
