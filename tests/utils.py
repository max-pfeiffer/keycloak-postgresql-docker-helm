"""Test utilities."""

from dataclasses import dataclass

from docker_image import reference


@dataclass
class ImageTagComponents:
    """Class containing image tag components."""

    registry: str
    image_name: str
    tag: str
    version: str
    keycloak_version: str

    @classmethod
    def create_from_reference(cls, tag: str):
        """Create and instance from image tag.

        :param tag:
        :return:
        """
        ref = reference.Reference.parse(tag)
        registry: str = ref.repository["domain"]
        image_name: str = ref.repository["path"]
        tag: str = ref["tag"]

        tag_parts: list[str] = tag.split("-")
        version: str = tag_parts[0]
        keycloak_version: str = tag_parts[1].lstrip("keycloak")
        return cls(
            registry=registry,
            image_name=image_name,
            tag=tag,
            version=version,
            keycloak_version=keycloak_version,
        )
