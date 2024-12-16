"""Basic test fixtures."""

from random import randrange

import pytest
from python_on_whales import Builder, DockerClient
from semver import VersionInfo
from testcontainers.postgres import PostgresContainer
from testcontainers.registry import DockerRegistryContainer

from build.utils import build_image, get_image_reference
from tests.constants import (
    POSTGRESQL_DATABASE_NAME,
    POSTGRESQL_PASSWORD,
    POSTGRESQL_USERNAME,
    REGISTRY_PASSWORD,
    REGISTRY_USERNAME,
)


@pytest.fixture(scope="session")
def docker_client() -> DockerClient:
    """Provide the Python on Whales docker client.

    :return:
    """
    return DockerClient(debug=True)


@pytest.fixture(scope="session")
def buildx_builder(docker_client: DockerClient) -> Builder:
    """Provide a Python on Whales BuildX builder instance.

    :param docker_client:
    :return:
    """
    builder: Builder = docker_client.buildx.create(
        driver="docker-container", driver_options=dict(network="host")
    )
    yield builder
    docker_client.buildx.stop(builder)
    docker_client.buildx.remove(builder)


@pytest.fixture(scope="session")
def image_version() -> str:
    """Generate a image version.

    :return:
    """
    image_version: str = str(
        VersionInfo(major=randrange(100), minor=randrange(100), patch=randrange(100))
    )
    return image_version


@pytest.fixture(scope="session")
def registry_container() -> DockerRegistryContainer:
    """Fixture for providing a running registry container.

    :return:
    """
    with DockerRegistryContainer(
        username=REGISTRY_USERNAME, password=REGISTRY_PASSWORD
    ).with_bind_ports(5000, 5000) as registry_container:
        yield registry_container


@pytest.fixture(scope="session")
def postgres_container() -> PostgresContainer:
    """Fixture for providing a PostgreSQL database container.

    :return:
    """
    with PostgresContainer(
        image="postgres:15",
        username=POSTGRESQL_USERNAME,
        password=POSTGRESQL_PASSWORD,
        dbname=POSTGRESQL_DATABASE_NAME,
    ).with_bind_ports(5432, 5432) as postgres_container:
        yield postgres_container


@pytest.fixture(scope="session")
def keycloak_image_reference(
    docker_client: DockerClient,
    buildx_builder: Builder,
    image_version: str,
    registry_container: DockerRegistryContainer,
) -> str:
    """Fixture building the Keycloak image and providing the image reference.

    :param docker_client:
    :param buildx_builder:
    :param image_version:
    :param registry_container:
    :return:
    """
    docker_client.login(
        server=registry_container.get_registry(),
        username=REGISTRY_USERNAME,
        password=REGISTRY_PASSWORD,
    )

    keycloak_version: str = "24.0.3"
    image_reference: str = get_image_reference(
        registry_container.get_registry(), keycloak_version
    )

    build_image(
        docker_client,
        buildx_builder,
        registry_container.get_registry(),
        keycloak_version,
    )
    yield image_reference
