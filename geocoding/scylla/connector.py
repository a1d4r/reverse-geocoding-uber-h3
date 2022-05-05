from typing import Any, Dict, Optional, Sequence, Union

from cassandra.cluster import ResponseFuture, ResultSet, Session
from cassandra.query import PreparedStatement, SimpleStatement
from loguru import logger

from geocoding import settings


class ScyllaConnector:
    def __init__(
        self,
        session: Session,
        max_concurrent_writes: int = 1000,
        max_concurrent_reads: int = 100,
        timeout: int = 60,
    ) -> None:
        """
        Arguments:
            session: Scylla session
            max_concurrent_writes: number of writes being executed without blocking
            max_concurrent_reads: number of reads being executed without blocking
            timeout: operation timeout, in seconds
        """
        self._session = session
        self._max_concurrent_writes = max_concurrent_writes
        self._max_concurrent_reads = (max_concurrent_reads,)
        self._timeout = timeout

    def prepare_cql_statement(self, cql_filename: str) -> PreparedStatement:
        with open(settings.CQL_QUERIES_PATH / cql_filename, "r") as f:
            return self._session.prepare(f.read())

    @staticmethod
    def _wait_futures(futures: list[ResponseFuture]) -> list[Exception]:
        """
        Wait for futures to execute.
        Return list of exceptions, if any, otherwise empty list.
        """
        exceptions = []
        for future in futures:
            try:
                future.result()
            except Exception as exc:  # pylint: disable=broad-except
                logger.exception("Query failed")
                exceptions.append(exc)
        return exceptions

    def execute(
        self,
        query: Union[PreparedStatement, SimpleStatement],
        params: Optional[Union[Sequence[Any], Dict[str, Any]]],
    ) -> ResultSet:
        """
        Execute query
        """
        return self._session.execute(query, params, timeout=self._timeout)

    def execute_concurrently(
        self,
        query: Union[PreparedStatement, SimpleStatement],
        params_list: list[Union[Sequence[Any], Dict[str, Any]]],
    ) -> list[Exception]:
        """
        Execute the same query with different parameters concurrently.
        Return list of exceptions, if any, otherwise empty list.
        """
        futures = []
        exceptions = []
        for i, params in enumerate(params_list):
            futures.append(
                self._session.execute_async(query, params, timeout=self._timeout)
            )
            if (i + 1) % self._max_concurrent_writes == 0:
                exceptions.extend(self._wait_futures(futures))
                futures = []
        logger.debug(
            "Succeed: {}, failed: {}",
            len(params_list) - len(exceptions),
            len(exceptions),
        )
        return exceptions
