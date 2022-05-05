from geocoding.models.cql import HexCountrySubdivision
from geocoding.storage.base import BaseStorage


class CountrySubdivisionsStorage(BaseStorage[HexCountrySubdivision]):
    """Storage layer for countries."""

    insert_query_name = "insert_subdivision.cql"
    cql_model_class = HexCountrySubdivision
