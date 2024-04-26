"""Build utilities."""

from pathlib import Path
from typing import Optional


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
