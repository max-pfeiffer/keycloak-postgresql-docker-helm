"""Contants for tests."""

from os import getenv

SLEEP_TIME: float = 4.0
REGISTRY_USERNAME: str = "foo"
REGISTRY_PASSWORD: str = "bar"

POSTGRESQL_USERNAME: str = "keycloak"
POSTGRESQL_PASSWORD: str = "supersecretpassword"
POSTGRESQL_DATABASE_NAME: str = "testdatabase"

KEYCLOAK_VERSION: str = getenv("KEYCLOAK_VERSION")
POSTGRESQL_VERSION: str = getenv("POSTGRESQL_VERSION")
