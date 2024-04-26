"""Tests for Docker image build."""

from pathlib import Path

from furl import furl
from httpx import BasicAuth, Response, get
from python_on_whales import Builder, DockerClient
from testcontainers.registry import DockerRegistryContainer

from build.constants import PLATFORMS
from build.utils import cache_settings, get_context, get_image_reference
from tests.constants import REGISTRY_PASSWORD, REGISTRY_USERNAME
from tests.utils import ImageTagComponents

BASIC_AUTH: BasicAuth = BasicAuth(REGISTRY_USERNAME, REGISTRY_PASSWORD)


def test_image_build(
    docker_client: DockerClient,
    buildx_builder: Builder,
    image_version: str,
    registry_container: DockerRegistryContainer,
) -> None:
    """Test for image build.

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
        registry_container.get_registry(), image_version, keycloak_version
    )
    context: Path = get_context()
    cache_to, cache_from = cache_settings(None, keycloak_version)

    docker_client.buildx.build(
        context_path=context,
        target="production-image",
        build_args={
            "KEYCLOAK_VERSION": keycloak_version,
        },
        tags=image_reference,
        platforms=PLATFORMS,
        builder=buildx_builder,
        cache_to=cache_to,
        cache_from=cache_from,
        push=True,
    )

    furl_item: furl = furl(f"http://{registry_container.get_registry()}")
    furl_item.path /= "v2/pfeiffermax/keycloak/tags/list"

    response: Response = get(furl_item.url, auth=BASIC_AUTH)

    assert response.status_code == 200

    response_image_tags: list[str] = response.json()["tags"]
    image_tag: str = ImageTagComponents.create_from_reference(image_reference).tag

    assert image_tag in response_image_tags
