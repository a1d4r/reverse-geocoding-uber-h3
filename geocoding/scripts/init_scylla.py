"""
Creating keyspace and tables in ScyllaDB.
"""
import os

from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from loguru import logger

from geocoding import settings
from geocoding.models.cql import HexCountry, HexCountrySubdivision
from geocoding.scylla.session import get_session


def initialize_scylla() -> None:
    if os.getenv("CQLENG_ALLOW_SCHEMA_MANAGEMENT") is None:
        os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"

    session = get_session()

    logger.info("Creating keyspace...")
    session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
        """
        % settings.SCYLLA_KEYSPACE
    )

    connection.set_session(get_session(settings.SCYLLA_KEYSPACE))

    logger.info("Creating tables...")
    sync_table(HexCountry)
    sync_table(HexCountrySubdivision)
    logger.info("Successfully initialized Scylla database!")


if __name__ == "__main__":
    initialize_scylla()
