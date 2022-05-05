from typing import Optional

from cassandra.cluster import Cluster, PlainTextAuthProvider, Session
from cassandra.query import named_tuple_factory
from loguru import logger

from geocoding import settings


def get_session(keyspace: Optional[str] = None) -> Session:
    cluster = Cluster(
        settings.SCYLLA_CLUSTER,
        protocol_version=3,
        auth_provider=PlainTextAuthProvider(
            username=settings.SCYLLA_USERNAME,
            password=settings.SCYLLA_PASSWORD,
        ),
    )

    logger.info(
        "Connecting to Scylla cluster: {} (keyspace: {})",
        settings.SCYLLA_CLUSTER,
        keyspace or "default",
    )

    session = cluster.connect(keyspace)
    session.row_factory = named_tuple_factory

    logger.info("Connected to Scylla cluster.")

    if cluster.is_shard_aware():
        logger.debug("Remote cluster supports shard awareness.")
    else:
        logger.debug("Remote cluster does not support shard awareness.")

    return session
