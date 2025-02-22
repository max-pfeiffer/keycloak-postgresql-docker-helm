"""Test fixtures for image publishing."""

import pytest
from click.testing import CliRunner
from testcontainers.registry import DockerRegistryContainer

from tests.constants import REGISTRY_PASSWORD, REGISTRY_USERNAME


@pytest.fixture(scope="package")
def publish_registry_container() -> DockerRegistryContainer:
    """Provide a Registry container locally for publishing the image.

    :return:
    """
    with DockerRegistryContainer(
        username=REGISTRY_USERNAME, password=REGISTRY_PASSWORD
    ).with_bind_ports(5000, 5000) as registry_container:
        yield registry_container


@pytest.fixture(scope="package")
def cli_runner() -> CliRunner:
    """Provide CLI runner for testing click CLI.

    :return:
    """
    runner = CliRunner()
    return runner
