"""Build utilities."""

from pathlib import Path
from typing import Optional

from python_on_whales import Builder, DockerClient

from build.constants import PLATFORMS


def get_context() -> Path:
    """Docker build context.

    :return:
    """
    return Path(__file__).parent.resolve()


def get_image_reference(
    registry: str,
    image_version: str,
    keycloak_version: str,
) -> str:
    """Docker Hub image reference.

    :param registry:
    :param image_version:
    :param keycloak_version:
    :return:
    """
    reference: str = (
        f"{registry}/pfeiffermax/keycloak:"
        f"{image_version}-keycloak{keycloak_version}"
    )
    return reference


def cache_settings(github_ref_name: Optional[str], keycloak_version: str) -> tuple:
    """Fixture for providing cache settings.

    :param github_ref_name:
    :param keycloak_version:
    :return:
    """
    cache_scope: str = f"{keycloak_version}"

    if github_ref_name:
        cache_to: str = f"type=gha,mode=max,scope={github_ref_name}-{cache_scope}"
        cache_from: str = f"type=gha,scope={github_ref_name}-{cache_scope}"
    else:
        cache_to = f"type=local,mode=max,dest=/tmp,scope={cache_scope}"
        cache_from = f"type=local,src=/tmp,scope={cache_scope}"

    return cache_to, cache_from


def build_image(
    docker_client: DockerClient,
    builder: Builder,
    registry: str,
    image_version: str,
    keycloak_version: str,
    github_ref_name: Optional[str] = None,
) -> None:
    """Build the Docker image.

    :param docker_client:
    :param builder:
    :param registry:
    :param image_version:
    :param keycloak_version:
    :param github_ref_name:
    :return:
    """
    context: Path = get_context()
    image_reference: str = get_image_reference(
        registry, image_version, keycloak_version
    )
    cache_to, cache_from = cache_settings(github_ref_name, keycloak_version)

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
