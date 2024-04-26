"""Basic test fixtures."""

from random import randrange

import pytest
from python_on_whales import Builder, DockerClient
from semver import VersionInfo
from testcontainers.postgres import PostgresContainer
from testcontainers.registry import DockerRegistryContainer

from tests.constants import REGISTRY_PASSWORD, REGISTRY_USERNAME


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
        username=REGISTRY_USERNAME, password=REGISTRY_PASSWORD, dbname="test"
    ).with_bind_ports(5432, 5432) as postgres_container:
        yield postgres_container
