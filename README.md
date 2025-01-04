[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![codecov](https://codecov.io/gh/max-pfeiffer/keycloak-postgresql-kubernetes/graph/badge.svg?token=ATRh4DIH7r)](https://codecov.io/gh/max-pfeiffer/keycloak-postgresql-kubernetes)
![pipeline workflow](https://github.com/max-pfeiffer/keycloak-postgresql-kubernetes/actions/workflows/pipeline.yml/badge.svg)
![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/pfeiffermax/keycloak-postgresql?sort=semver)
![Docker Pulls](https://img.shields.io/docker/pulls/pfeiffermax/keycloak-postgresql)
# Keycloak PostgreSQL Kubernetes
Docker image and Helm charts for running Keycloak with PostgreSQL database on Kubernetes.

## Docker Image
Features:
* PostgreSQL database backend
* Health checks enabled
* Metrics enabled

**Docker Hub:** [https://hub.docker.com/r/pfeiffermax/keycloak-postgresql](https://hub.docker.com/r/pfeiffermax/keycloak-postgresql)

## Helm Charts
Use the Helm charts to install Keycloak with this Docker Image on Kubernetes:
```shell
helm repo add keycloak-postgres https://max-pfeiffer.github.io/keycloak-postgresql-helm
helm install postgresql keycloak-postgres/postgresql
helm install keycloak keycloak-postgres/keycloak
```

For further documentation and examples see:
* [Keycloak Helm Chart](charts%2Fkeycloak%2FREADME.md)
* [PostgreSQL Helm Chart](charts%2Fpostgresql%2FREADME.md)
