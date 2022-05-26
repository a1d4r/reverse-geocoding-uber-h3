"""
Fill country subdivisions corresponding to H3 hexagon IDs in Scylla.
"""
from loguru import logger

from geocoding import settings
from geocoding.convertors.h3 import fill_polygons_by_hexagons
from geocoding.extractors.gadm import GADMCountrySubdivisionsExtractor
from geocoding.scylla.connector import ScyllaConnector
from geocoding.scylla.session import get_session
from geocoding.storage import CountrySubdivisionsStorage
from geocoding.utils import timeit

logger.add(settings.LOGS_DIR / "file_{time}.log")


@timeit
def fill_subdivisions() -> None:
    session = get_session(settings.SCYLLA_KEYSPACE)
    scylla = ScyllaConnector(session)
    storage = CountrySubdivisionsStorage(scylla)

    total_number_of_hexagons = 0
    extractor = GADMCountrySubdivisionsExtractor(path=settings.GADM_DATASET_PATH)
    for subdivision in extractor:
        logger.info(
            "{} - {} - Filling with polygons",
            subdivision.country_name,
            subdivision.name,
        )
        hex_ids = fill_polygons_by_hexagons(
            subdivision.geometry, settings.SUBDIVISIONS_H3_RESOLUTION
        )
        logger.info(
            "{} - {} - Filled by {} hexagons",
            subdivision.country_name,
            subdivision.name,
            len(hex_ids),
        )
        cql_subdivisions = []
        if hex_ids:
            total_number_of_hexagons += len(hex_ids)
            for hex_id in hex_ids:
                cql_subdivisions.append(subdivision.to_cql_model(hex_id))
            logger.info(
                "{} - {} - Writing to database",
                subdivision.country_name,
                subdivision.name,
            )
            storage.insert_many(cql_subdivisions)

    logger.info("Inserted {} hexagons into database", total_number_of_hexagons)


if __name__ == "__main__":
    fill_subdivisions()
