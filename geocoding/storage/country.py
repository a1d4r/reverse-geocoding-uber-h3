from geocoding.models.cql import HexCountry
from geocoding.storage.base import BaseStorage


class CountriesStorage(BaseStorage[HexCountry]):
    """Storage layer for countries."""

    insert_query_name = "insert_country.cql"
    read_query_name = "read_country.cql"
    cql_model_class = HexCountry
