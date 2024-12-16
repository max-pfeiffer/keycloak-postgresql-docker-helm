"""Tests for Docker image build."""

from furl import furl
from httpx import BasicAuth, Response, get
from testcontainers.registry import DockerRegistryContainer

from tests.constants import REGISTRY_PASSWORD, REGISTRY_USERNAME
from tests.utils import ImageTagComponents

BASIC_AUTH: BasicAuth = BasicAuth(REGISTRY_USERNAME, REGISTRY_PASSWORD)


def test_image_build(
    keycloak_image_reference: str,
    registry_container: DockerRegistryContainer,
) -> None:
    """Test for image build.

    :param keycloak_image_reference:
    :param registry_container:
    :return:
    """
    furl_item: furl = furl(f"http://{registry_container.get_registry()}")
    furl_item.path /= "v2/pfeiffermax/keycloak-postgresql/tags/list"

    response: Response = get(furl_item.url, auth=BASIC_AUTH)

    assert response.status_code == 200

    response_image_tags: list[str] = response.json()["tags"]
    image_tag: str = ImageTagComponents.create_from_reference(
        keycloak_image_reference
    ).tag

    assert image_tag in response_image_tags
