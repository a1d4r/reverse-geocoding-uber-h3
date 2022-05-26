"""
Fill countries corresponding to H3 hexagon IDs in Scylla.
"""
from loguru import logger

from geocoding import settings
from geocoding.convertors.h3 import fill_polygons_by_hexagons
from geocoding.extractors.gadm import GADMCountriesExtractor
from geocoding.scylla.connector import ScyllaConnector
from geocoding.scylla.session import get_session
from geocoding.storage import CountriesStorage
from geocoding.utils import timeit

logger.add(settings.LOGS_DIR / "file_{time}.log")


@timeit
def fill_countries() -> None:
    session = get_session(settings.SCYLLA_KEYSPACE)
    scylla = ScyllaConnector(session)
    storage = CountriesStorage(scylla)

    total_number_of_hexagons = 0
    extractor = GADMCountriesExtractor(path=settings.GADM_DATASET_PATH)
    for country in extractor:
        logger.info("{} - Filling with polygons", country.name)
        hex_ids = fill_polygons_by_hexagons(
            country.geometry, settings.COUNTRIES_H3_RESOLUTION
        )
        logger.info("{} - Filled by {} hexagons", country.name, len(hex_ids))
        cql_countries = []
        if hex_ids:
            total_number_of_hexagons += len(hex_ids)
            for hex_id in hex_ids:
                cql_countries.append(country.to_cql_model(hex_id))
            logger.info("{} - Writing to database", country.name)
            storage.insert_many(cql_countries)
    logger.info("Inserted {} hexagons into database", total_number_of_hexagons)


if __name__ == "__main__":
    fill_countries()
