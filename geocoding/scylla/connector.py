from typing import Any, Dict, Optional, Sequence, Union

from cassandra.cluster import ResponseFuture, ResultSet, Session
from cassandra.query import PreparedStatement, SimpleStatement

from geocoding import settings


class ScyllaConnector:
    def __init__(
        self,
        session: Session,
        _max_concurrent_queries: int = settings.SCYLLA_CONCURRENT_QUERIES,
        timeout: int = settings.SCYLLA_TIMEOUT,
    ) -> None:
        """
        Arguments:
            session: Scylla session
            _max_concurrent_queries: number of queries being executed without blocking
            timeout: operation timeout, in seconds
        """
        self._session = session
        self._max_concurrent_queries = _max_concurrent_queries
        self._timeout = timeout

    def prepare_cql_statement(self, cql_filename: str) -> PreparedStatement:
        with open(settings.CQL_QUERIES_DIR / cql_filename, "r") as f:
            return self._session.prepare(f.read())

    @staticmethod
    def _wait_futures(
        futures: list[ResponseFuture],
    ) -> list[Union[Exception, ResultSet]]:
        """
        Wait for futures to execute.
        Return list of results. Each result is either ResultSet or Exception
        """
        results = []
        for future in futures:
            try:
                results.append(future.result())
            except Exception as exc:  # pylint: disable=broad-except
                results.append(exc)
        return results

    def execute(
        self,
        query: Union[PreparedStatement, SimpleStatement],
        params: Optional[Union[Sequence[Any], Dict[str, Any]]],
    ) -> ResultSet:
        """
        Execute query with specified parameters
        """
        return self._session.execute(query, params, timeout=self._timeout)

    def execute_concurrently(
        self,
        query: Union[PreparedStatement, SimpleStatement],
        params_list: list[Union[Sequence[Any], Dict[str, Any]]],
    ) -> list[Union[Exception, ResultSet]]:
        """
        Execute the same query with different parameters concurrently.
        Return list of results. Each result is either ResultSet or Exception
        """
        results = []
        futures = []
        for i, params in enumerate(params_list):
            futures.append(
                self._session.execute_async(query, params, timeout=self._timeout)
            )
            if (i + 1) % self._max_concurrent_queries == 0:
                results.extend(self._wait_futures(futures))
                futures = []
        results.extend(self._wait_futures(futures))
        return results
