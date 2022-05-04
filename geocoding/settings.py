from pathlib import Path

CQL_QUERIES_PATH = Path(__file__).parent.parent.resolve() / "cql"

SCYLLA_KEYSPACE: str = "geo"
SCYLLA_CLUSTER: list[str] = ["127.0.0.1"]
SCYLLA_USERNAME: str = "cassandra"
SCYLLA_PASSWORD: str = "cassandra"
