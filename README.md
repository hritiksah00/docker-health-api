# Docker Health API

[![Docker API CI](https://github.com/hritiksah00/docker-health-api/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/hritiksah00/docker-health-api/actions/workflows/ci.yml)

A small Flask API for practising Docker packaging, container health checks, and HTTP integration testing. Docker Compose runs the application locally, and GitHub Actions builds and tests it on pushes and pull requests.

This is a learning project that runs on your own computer. An AWS account is not required.

## What it demonstrates

- Packaging a Python application and its pinned dependencies in a Docker image.
- Starting the API with Compose and publishing its port on localhost.
- Probing the running application with a Docker health check.
- Testing real HTTP responses using Python's standard library.
- Running the build and integration tests in GitHub Actions.

## Requirements

- Docker Engine running, with the Docker Compose and Buildx plugins.
- Python 3 on the host for integration tests; CI uses Python 3.13.
- Git and `curl`.
- Port 5000 available on the host.
- Internet access for the initial image and dependency downloads.

Check the Docker tools:

```bash
docker version
docker compose version
docker buildx version
```

## Run locally

```bash
git clone https://github.com/hritiksah00/docker-health-api.git
cd docker-health-api

docker compose up -d --build --wait --wait-timeout 60
docker compose ps
curl -i http://127.0.0.1:5000/health
```

A successful start shows the `api` container as `healthy`. The health endpoint returns HTTP `200` and:

```json
{"status":"ok"}
```

Compose publishes `127.0.0.1:5000:5000`, binding the host port to localhost. Flask listens on `0.0.0.0:5000` inside the container so Docker can forward requests to it.

## Endpoints

| Method | Path | JSON response |
| --- | --- | --- |
| GET | `/` | `{"service":"docker-health-api","message":"My first container project"}` |
| GET | `/health` | `{"status":"ok"}` |

## Run the integration tests

Keep the Compose application running, then execute:

```bash
python3 -m unittest discover -s tests -v
```

The two tests send real HTTP requests to `127.0.0.1:5000`. Both verify HTTP `200` and a JSON content type. The health test checks the complete response body; the home test checks the service name.

The host-side tests use only Python's standard library. Flask and its dependencies are installed inside the image.

## Health check and CI

The Dockerfile contains two separate commands:

- The final `CMD` starts Flask.
- `HEALTHCHECK` periodically requests `/health` from inside the container.

The health probe is configured with a 30-second interval, a 3-second timeout, a 5-second start period, and 3 retries. It uses Python's `urllib.request`, so the image does not need `curl`.

The [CI workflow](.github/workflows/ci.yml) runs on pushes, pull requests, and manual dispatch. It builds the image, starts Compose and waits for health, runs both integration tests, displays container logs, and tears down the containers. It does not publish a live API.

## Everyday commands

View application and health-probe requests:

```bash
docker compose logs --tail 30 api
```

Rebuild and start after changing the application or Dockerfile:

```bash
docker compose up -d --build --wait --wait-timeout 60
```

Stop and remove this project's Compose containers and network:

```bash
docker compose down
```

The built image and source files remain available.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Port 5000 is already allocated | Check `docker ps` and any locally running Flask process. Stop the application already using that port before starting Compose. |
| A container remains unhealthy | Read `docker compose logs --tail 30 api`. Confirm that the Dockerfile still has its final Flask `CMD`; adding `HEALTHCHECK` does not start the server. |
| Tests report connection refused | Run `docker compose ps` and confirm that the API is running and healthy before testing. |
| `docker compose` or `docker buildx` is unknown | Install the matching plugins for your Docker installation. On the Ubuntu `docker.io` setup used for this project, the packages were `docker-compose-v2` and `docker-buildx`. |
| An older `docker run` command reports a name conflict | Container names remain reserved when containers stop. `docker start` reuses an existing container; `docker run` creates a new one. Compose manages this project's containers for the setup above. |

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Flask routes and JSON responses |
| `requirements.txt` | Pinned Python application dependencies |
| `Dockerfile` | Image build, health probe, and startup command |
| `compose.yaml` | Local service build and port mapping |
| `tests/test_api.py` | HTTP integration tests |
| `.github/workflows/ci.yml` | Automated image build and integration checks |

## Current scope

The application uses Flask's development server and is intended for local learning. The `/health` endpoint is a basic liveness check: it does not inspect a database or other dependencies. Docker reports the health state; a failing health check alone does not automatically restart the container.

The project demonstrates containerization and CI. It does not claim a production deployment, external monitoring, or measured availability.
