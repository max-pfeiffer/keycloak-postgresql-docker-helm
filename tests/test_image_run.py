"""Tests running the Keycloak image."""

from pathlib import Path
from tempfile import TemporaryDirectory
from time import time

import pytest
import trustme
from httpx import Client, ConnectError, ConnectTimeout, Response
from python_on_whales import DockerClient
from testcontainers.postgres import PostgresContainer

from tests.constants import (
    POSTGRESQL_DATABASE_NAME,
    POSTGRESQL_PASSWORD,
    POSTGRESQL_USERNAME,
)
from tests.utils import running_on_github_actions


@pytest.mark.skipif(
    running_on_github_actions(),
    reason="Connection Error for Keycloak Container on GitHub",
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

    # Since v25.0 Keycloak health checks are exposed on management port 9000 by default
    # See: https://www.keycloak.org/server/health
    keycloak_management_port: int = 9000

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
            "KC_DB_USERNAME": POSTGRESQL_USERNAME,
            "KC_DB_PASSWORD": POSTGRESQL_PASSWORD,
            "KC_DB_URL_HOST": "host.docker.internal",
            "KC_DB_URL_DATABASE": POSTGRESQL_DATABASE_NAME,
            "KC_HTTPS_CERTIFICATE_FILE": str(certificate_pem),
            "KC_HTTPS_CERTIFICATE_KEY_FILE": str(private_key_pem),
            "KEYCLOAK_ADMIN": "admin",
            "KEYCLOAK_ADMIN_PASSWORD": "admin",
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

        with docker_client.container.run(
            keycloak_image_reference,
            envs=environment_variables,
            volumes=volumes,
            command=["start", "--optimized"],
            platform="linux/amd64",
            detach=True,
            interactive=True,
            tty=True,
            publish=[(443, 8443), (keycloak_management_port, keycloak_management_port)],
        ) as keycloak_container:
            assert keycloak_container.state.status == "running"
            ready_status_code = None

            with ca.cert_pem.tempfile() as ca_temp_path:
                client = Client(verify=ca_temp_path)
                timeout = time() + 60

                while ready_status_code != 200:
                    try:
                        response: Response = client.get(
                            f"https://{hostname}:{keycloak_management_port}/health/ready",
                            timeout=1,
                        )
                        ready_status_code = response.status_code
                    except (TimeoutError, ConnectError, ConnectTimeout) as exc:
                        ready_status_code = str(exc)

                    if time() > timeout:
                        break

            assert ready_status_code == 200
