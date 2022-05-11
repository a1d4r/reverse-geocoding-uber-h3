from typing import Generic, Optional, TypeVar, cast

from abc import abstractmethod

from cassandra.cqlengine.models import Model as CQLModel
from loguru import logger

from geocoding.models.cql import HexCountry, HexCountrySubdivision
from geocoding.scylla.connector import ScyllaConnector

CQLModelType = TypeVar("CQLModelType", bound=CQLModel)


class BaseStorage(Generic[CQLModelType]):
    """
    Storage layer for geographic entities represented as CQL models.
    """

    def __init__(self, scylla_connector: ScyllaConnector) -> None:
        self._scylla = scylla_connector
        self._insert_query = self._scylla.prepare_cql_statement(self.insert_query_name)
        self._read_query = self._scylla.prepare_cql_statement(self.read_query_name)

    @property
    @abstractmethod
    def insert_query_name(self) -> str:
        """File name of CQL insert query, must end with .cql"""

    @property
    @abstractmethod
    def read_query_name(self) -> str:
        """File name of CQL read query, must end with .cql"""

    @property
    @abstractmethod
    def cql_model_class(self) -> type[CQLModelType]:
        """Class of CQL model which will be saved and retrieved."""

    def insert(self, cql_object: CQLModelType) -> None:
        """Insert a single record in the database."""
        self._scylla.execute(self._insert_query, list(cql_object.values()))

    def insert_many(self, cql_objects: list[CQLModelType]) -> None:
        """Insert multiple records in the database."""
        results = self._scylla.execute_concurrently(
            self._insert_query,
            [list(cql_object.values()) for cql_object in cql_objects],
        )
        for cql_object, result in zip(cql_objects, results):
            if isinstance(result, Exception):
                logger.error(
                    "Failed to insert row {}: {}", repr(cql_object), repr(result)
                )

    def read(self, hex_id: int) -> Optional[CQLModelType]:
        """Read record by ID of hexagon."""
        result = list(self._scylla.execute(self._read_query, [hex_id]))
        if result:
            return cast(CQLModelType, self.cql_model_class(**result[0]))
        return None

    def read_many(self, hex_ids: list[int]) -> dict[int, Optional[CQLModelType]]:
        """Read multiple records by IDs of hexagons."""
        results = self._scylla.execute_concurrently(
            self._read_query,
            [[hex_id] for hex_id in hex_ids],
        )
        results_by_hex_id = {hex_id: None for hex_id in hex_ids}
        for hex_id, result in zip(hex_ids, results):
            if isinstance(result, Exception):
                logger.error(
                    "Failed to retrieve row by hex_id={}: {}", hex_id, repr(result)
                )
            elif result:
                cql_obj = cast(CQLModelType, self.cql_model_class(**result[0]))
                results_by_hex_id[hex_id] = cql_obj
        return results_by_hex_id


class CountriesStorage(BaseStorage[HexCountry]):
    """Storage layer for countries."""

    insert_query_name = "insert_country.cql"
    read_query_name = "read_country.cql"
    cql_model_class = HexCountry


class CountrySubdivisionsStorage(BaseStorage[HexCountrySubdivision]):
    """Storage layer for countries."""

    insert_query_name = "insert_subdivision.cql"
    read_query_name = "read_subdivision.cql"
    cql_model_class = HexCountrySubdivision
