"""
Creating keyspace and tables in ScyllaDB.
"""
import os

from cassandra.cluster import Cluster, PlainTextAuthProvider
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from loguru import logger

from geocoding import settings
from geocoding.db.models import HexCountry, HexCountrySubdivision


def initialize_scylla() -> None:
    if os.getenv("CQLENG_ALLOW_SCHEMA_MANAGEMENT") is None:
        os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"

    cluster = Cluster(
        settings.SCYLLA_CLUSTER,
        protocol_version=3,
        auth_provider=PlainTextAuthProvider(
            username=settings.SCYLLA_USERNAME,
            password=settings.SCYLLA_PASSWORD,
        ),
    )

    logger.info("Connecting to Scylla cluster...")
    session = cluster.connect()

    logger.info("Creating keyspace...")
    session.execute(
        f"""
        CREATE KEYSPACE IF NOT EXISTS {settings.SCYLLA_KEYSPACE}
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
        """
    )

    logger.info("Connecting to keyspace...")
    session = cluster.connect(settings.SCYLLA_KEYSPACE)
    connection.set_session(session)

    logger.info("Creating tables...")
    sync_table(HexCountry)
    sync_table(HexCountrySubdivision)
    logger.info("Successfully initialized Scylla database!")


if __name__ == "__main__":
    initialize_scylla()
