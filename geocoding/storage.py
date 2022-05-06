from typing import Generic, Optional, TypeVar, cast

from abc import abstractmethod

from cassandra.cqlengine.models import Model as CQLModel

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
        self._scylla.execute_concurrently(
            self._insert_query,
            [list(cql_object.values()) for cql_object in cql_objects],
        )

    def read(self, hex_id: int) -> Optional[CQLModelType]:
        """Read record by hex_id."""
        result = list(self._scylla.execute(self._read_query, [hex_id]))
        if result:
            return cast(CQLModelType, self.cql_model_class(**result[0]))
        return None


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
