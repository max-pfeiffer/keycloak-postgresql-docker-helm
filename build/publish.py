"""Publish CLI."""

from os import getenv

import click
from python_on_whales import Builder, DockerClient

from build.utils import build_image


@click.command()
@click.option(
    "--docker-hub-username",
    envvar="DOCKER_HUB_USERNAME",
    help="Docker Hub username",
)
@click.option(
    "--docker-hub-password",
    envvar="DOCKER_HUB_PASSWORD",
    help="Docker Hub password",
)
@click.option("--version-tag", envvar="GIT_TAG_NAME", required=True, help="Version tag")
@click.option(
    "--registry", envvar="REGISTRY", default="docker.io", help="Docker registry"
)
def main(
    docker_hub_username: str,
    docker_hub_password: str,
    version_tag: str,
    keycloak_version: str,
    registry: str,
) -> None:
    """Build and publish image to Docker Hub.

    :param docker_hub_username:
    :param docker_hub_password:
    :param version_tag:
    :param keycloak_version:
    :param registry:
    :return:
    """
    github_ref_name: str = getenv("GITHUB_REF_NAME")

    docker_client: DockerClient = DockerClient()
    builder: Builder = docker_client.buildx.create(
        driver="docker-container", driver_options=dict(network="host")
    )

    docker_client.login(
        server=registry,
        username=docker_hub_username,
        password=docker_hub_password,
    )

    build_image(
        docker_client,
        builder,
        registry,
        version_tag,
        keycloak_version,
        github_ref_name=github_ref_name,
    )

    # Cleanup
    docker_client.buildx.stop(builder)
    docker_client.buildx.remove(builder)


if __name__ == "__main__":
    main()
