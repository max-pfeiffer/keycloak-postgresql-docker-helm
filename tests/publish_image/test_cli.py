"""Tests for building and publishing the image using CLI and command line arguments."""

from click.testing import CliRunner, Result
from python_on_whales import DockerException
from testcontainers.registry import DockerRegistryContainer

from build.publish import main
from tests.constants import KEYCLOAK_VERSION, REGISTRY_PASSWORD, REGISTRY_USERNAME


def test_registry_with_credentials(
    publish_registry_container: DockerRegistryContainer,
    cli_runner: CliRunner,
):
    """Test building and publishing the image to a Docker registry.

    The registry requires authentication. It requires authentication for this case.

    :param publish_registry_container:
    :param cli_runner:
    :return:
    """
    result: Result = cli_runner.invoke(
        main,
        args=[
            "--docker-hub-username",
            REGISTRY_USERNAME,
            "--docker-hub-password",
            REGISTRY_PASSWORD,
            "--keycloak-version",
            KEYCLOAK_VERSION,
            "--registry",
            publish_registry_container.get_registry(),
        ],
    )
    assert result.exit_code == 0


def test_registry_with_wrong_credentials(
    publish_registry_container: DockerRegistryContainer,
    cli_runner: CliRunner,
):
    """Test building and publishing the image to a Docker registry.

    The registry requires authentication. The credentials are invalid in this case.

    :param publish_registry_container:
    :param cli_runner:
    :return:
    """
    result: Result = cli_runner.invoke(
        main,
        args=[
            "--docker-hub-username",
            "bang",
            "--docker-hub-password",
            "boom",
            "--keycloak-version",
            KEYCLOAK_VERSION,
            "--registry",
            publish_registry_container.get_registry(),
        ],
    )
    assert result.exit_code == 1
    assert isinstance(result.exception, DockerException)
