"""Test fixtures for image build tests."""

import pytest
from python_on_whales import Builder, DockerClient
from testcontainers.postgres import PostgresContainer
from testcontainers.registry import DockerRegistryContainer

from build.utils import build_image, get_image_reference
from tests.constants import (
    KEYCLOAK_VERSION,
    POSTGRESQL_DATABASE_NAME,
    POSTGRESQL_PASSWORD,
    POSTGRESQL_USERNAME,
    POSTGRESQL_VERSION,
    REGISTRY_PASSWORD,
    REGISTRY_USERNAME,
)


@pytest.fixture(scope="package")
def registry_container() -> DockerRegistryContainer:
    """Fixture for providing a running registry container.

    :return:
    """
    with DockerRegistryContainer(
        username=REGISTRY_USERNAME, password=REGISTRY_PASSWORD
    ).with_bind_ports(5000, 5000) as registry_container:
        yield registry_container


@pytest.fixture(scope="package")
def postgres_container() -> PostgresContainer:
    """Fixture for providing a PostgreSQL database container.

    :return:
    """
    with PostgresContainer(
        image=f"postgres:{POSTGRESQL_VERSION}",
        username=POSTGRESQL_USERNAME,
        password=POSTGRESQL_PASSWORD,
        dbname=POSTGRESQL_DATABASE_NAME,
    ).with_bind_ports(5432, 5432) as postgres_container:
        yield postgres_container


@pytest.fixture(scope="package")
def keycloak_image_reference(
    docker_client: DockerClient,
    buildx_builder: Builder,
    registry_container: DockerRegistryContainer,
) -> str:
    """Fixture building the Keycloak image and providing the image reference.

    :param docker_client:
    :param buildx_builder:
    :param registry_container:
    :return:
    """
    docker_client.login(
        server=registry_container.get_registry(),
        username=REGISTRY_USERNAME,
        password=REGISTRY_PASSWORD,
    )

    image_reference: str = get_image_reference(
        registry_container.get_registry(), KEYCLOAK_VERSION
    )

    build_image(
        docker_client,
        buildx_builder,
        registry_container.get_registry(),
        KEYCLOAK_VERSION,
    )
    yield image_reference
