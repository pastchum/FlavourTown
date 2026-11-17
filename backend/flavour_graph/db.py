from __future__ import annotations

from typing import Any, Optional

from neo4j import Driver, GraphDatabase

from .config import settings

_driver: Optional[Driver] = None


def get_driver() -> Driver:
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(
            settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password)
        )
    return _driver


def close_driver() -> None:
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None


def read(query: str, **params: Any) -> list[dict[str, Any]]:
    records, _, _ = get_driver().execute_query(query, params, routing_="r")
    return [r.data() for r in records]


def write(query: str, **params: Any) -> None:
    get_driver().execute_query(query, params)
