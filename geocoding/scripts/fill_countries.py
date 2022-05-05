"""
Fill countries corresponding to H3 hexagon IDs in Scylla.
"""
from loguru import logger

from geocoding import settings
from geocoding.extractors.gadm import GADMCountriesExtractor
from geocoding.processing.h3 import fill_polygons_by_hexagons
from geocoding.scylla.connector import ScyllaConnector
from geocoding.scylla.session import get_session
from geocoding.storage.countries import CountriesStorage

logger.add(settings.LOGS_DIR / "file_{time}.log")


def fill_countries() -> None:
    session = get_session(settings.SCYLLA_KEYSPACE)
    scylla = ScyllaConnector(session)
    storage = CountriesStorage(scylla)

    extractor = GADMCountriesExtractor(path=settings.GADM_DATASET_PATH)
    for country in extractor:
        logger.info("{} - Filling with polygons", country.name)
        hex_ids = fill_polygons_by_hexagons(
            country.geometry, settings.COUNTRIES_H3_RESOLUTION
        )
        logger.info("{} - Filled by {} hexagons", country.name, len(hex_ids))
        cql_countries = []
        if hex_ids:
            for hex_id in hex_ids:
                cql_countries.append(country.to_cql_model(hex_id))
            logger.info("{} - Writing to database", country.name)
            storage.insert_many(cql_countries)

    logger.info("Done")


if __name__ == "__main__":
    fill_countries()
