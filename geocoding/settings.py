from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
CQL_QUERIES_DIR = PROJECT_ROOT / "cql"
LOGS_DIR = PROJECT_ROOT / "logs"
GADM_DATASET_PATH = Path("/Users/a-garikhanov/Documents/gadm36_levels_shp")

SCYLLA_KEYSPACE: str = "geo"
SCYLLA_CLUSTER: list[str] = ["127.0.0.1"]
SCYLLA_USERNAME: str = "cassandra"
SCYLLA_PASSWORD: str = "cassandra"

SCYLLA_CONCURRENT_READS = 1000
SCYLLA_CONCURRENT_WRITES = 5000
SCYLLA_TIMEOUT = 60  # in seconds

COUNTRIES_H3_RESOLUTION: int = 5
SUBDIVISIONS_H3_RESOLUTION: int = 5
