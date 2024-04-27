"""Tests running the Keycloak image."""

from pathlib import Path
from tempfile import TemporaryDirectory

import trustme
from httpx import Client, ConnectError, ConnectTimeout, Response
from python_on_whales import Container, DockerClient
from testcontainers.postgres import PostgresContainer

from tests.constants import (
    POSTGRESQL_DATABASE_NAME,
    POSTGRESQL_PASSWORD,
    POSTGRESQL_USERNAME,
)


def test_image_run(
    docker_client: DockerClient,
    keycloak_image_reference: str,
    postgres_container: PostgresContainer,
) -> None:
    """Test running the Keycloak container with PostgreSQL database.

    :param docker_client:
    :param keycloak_image_reference:
    :param postgres_container:
    :return:
    """
    hostname: str = "localhost"

    ca = trustme.CA()
    server_cert = ca.issue_cert(hostname)

    with TemporaryDirectory() as temp_directory_name:
        file_name_key: str = "key.pem"
        file_name_certificate: str = "certificate.pem"

        temp_directory: Path = Path(temp_directory_name)
        temp_private_key_pem: Path = temp_directory / file_name_key
        temp_certificate_pem: Path = temp_directory / file_name_certificate

        server_cert.private_key_pem.write_to_path(temp_private_key_pem)
        server_cert.cert_chain_pems[0].write_to_path(temp_certificate_pem)

        pem_files_directory: Path = Path("/opt/keycloak/conf")
        private_key_pem: Path = pem_files_directory / file_name_key
        certificate_pem: Path = pem_files_directory / file_name_certificate

        # For configuration details see:
        # https://www.keycloak.org/server/db
        # https://www.keycloak.org/server/enabletls
        environment_variables: dict = {
            "KC_HOSTNAME": hostname,
            "KC_DB": "postgres",
            "KC_DB_USERNAME": POSTGRESQL_USERNAME,
            "KC_DB_PASSWORD": POSTGRESQL_PASSWORD,
            "KC_DB_URL_HOST": "host.docker.internal",
            "KC_DB_URL_DATABASE": POSTGRESQL_DATABASE_NAME,
            "KC_HTTPS_CERTIFICATE_FILE": str(certificate_pem),
            "KC_HTTPS_CERTIFICATE_KEY_FILE": str(private_key_pem),
            "KC_HTTPS_PORT": "443",
            "KEYCLOAK_ADMIN": "admin",
            "KEYCLOAK_ADMIN_PASSWORD": "admin",
            "KC_HEALTH_ENABLED": "true",
        }
        volumes: list = [
            (
                str(temp_private_key_pem),
                str(private_key_pem),
            ),
            (
                str(temp_certificate_pem),
                str(certificate_pem),
            ),
        ]

        keycloak_container: Container = docker_client.container.run(
            keycloak_image_reference,
            envs=environment_variables,
            volumes=volumes,
            # command=["start", "--optimized"],
            command=["start"],
            detach=True,
            publish=[(443, 443)],
        )
        assert keycloak_container

        ready_status_code = None

        with ca.cert_pem.tempfile() as ca_temp_path:
            client = Client(verify=ca_temp_path)

            while ready_status_code != 200:
                try:
                    response: Response = client.get(
                        f"https://{hostname}/health/ready", timeout=1
                    )
                    ready_status_code = response.status_code
                except (TimeoutError, ConnectError, ConnectTimeout):
                    pass

        assert ready_status_code == 200

        # Tear down
        keycloak_container.stop()
        keycloak_container.remove()
