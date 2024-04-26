"""Publish CLI."""

from os import getenv
from pathlib import Path

import click
from python_on_whales import Builder, DockerClient

from build.constants import PLATFORMS
from build.utils import cache_settings, get_context, get_image_reference


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
    context: Path = get_context()
    image_reference: str = get_image_reference(registry, version_tag, keycloak_version)
    cache_to, cache_from = cache_settings(github_ref_name, keycloak_version)

    docker_client: DockerClient = DockerClient()
    builder: Builder = docker_client.buildx.create(
        driver="docker-container", driver_options=dict(network="host")
    )

    docker_client.login(
        server=registry,
        username=docker_hub_username,
        password=docker_hub_password,
    )

    docker_client.buildx.build(
        context_path=context,
        target="production-image",
        build_args={
            "KEYCLOAK_VERSION": keycloak_version,
        },
        tags=image_reference,
        platforms=PLATFORMS,
        builder=builder,
        cache_to=cache_to,
        cache_from=cache_from,
        push=True,
    )

    # Cleanup
    docker_client.buildx.stop(builder)
    docker_client.buildx.remove(builder)


if __name__ == "__main__":
    main()
