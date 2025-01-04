[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![codecov](https://codecov.io/gh/max-pfeiffer/keycloak-postgresql-docker-helm/graph/badge.svg?token=ATRh4DIH7r)](https://codecov.io/gh/max-pfeiffer/keycloak-postgresql-docker-helm)
![pipeline workflow](https://github.com/max-pfeiffer/keycloak-postgresql-docker-helm/actions/workflows/pipeline.yml/badge.svg)
![helm-release workflow](https://github.com/max-pfeiffer/keycloak-postgresql-docker-helm/actions/workflows/helm-release.yaml/badge.svg)
![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/pfeiffermax/keycloak-postgresql?sort=semver)
![Docker Pulls](https://img.shields.io/docker/pulls/pfeiffermax/keycloak-postgresql)
# Keycloak PostgreSQL Docker Image and Helm Charts 
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
helm repo add keycloak-postgresql https://max-pfeiffer.github.io/keycloak-postgresql-docker-helm
helm install postgresql keycloak-postgresql/postgresql --values your_values.yaml --namespace your-namespace
helm install keycloak keycloak-postgresql/keycloak --values your_values.yaml --namespace your-namespace
```

For further documentation and `values.yaml` examples see:
* [Keycloak Helm Chart](charts%2Fkeycloak%2FREADME.md)
* [PostgreSQL Helm Chart](charts%2Fpostgresql%2FREADME.md)
