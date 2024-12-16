"""Build utilities."""

from pathlib import Path

from python_on_whales import Builder, DockerClient

from build.constants import PLATFORMS


def get_context() -> Path:
    """Docker build context.

    :return:
    """
    return Path(__file__).parent.resolve()


def get_image_reference(
    registry: str,
    keycloak_version: str,
) -> str:
    """Docker Hub image reference.

    :param registry:
    :param keycloak_version:
    :return:
    """
    reference: str = f"{registry}/pfeiffermax/keycloak-postgresql:{keycloak_version}"
    return reference


def build_image(
    docker_client: DockerClient,
    builder: Builder,
    registry: str,
    keycloak_version: str,
) -> None:
    """Build the Docker image.

    :param docker_client:
    :param builder:
    :param registry:
    :param keycloak_version:
    :return:
    """
    context: Path = get_context()
    image_reference: str = get_image_reference(registry, keycloak_version)

    docker_client.buildx.build(
        context_path=context,
        target="production-image",
        build_args={
            "KEYCLOAK_VERSION": keycloak_version,
        },
        tags=image_reference,
        platforms=PLATFORMS,
        builder=builder,
        push=True,
    )
