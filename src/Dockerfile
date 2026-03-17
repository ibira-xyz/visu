# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.13.12-alpine3.22 AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app
COPY pyproject.toml /app
COPY uv.lock /app

RUN uv sync --no-dev --frozen

FROM --platform=$BUILDPLATFORM python:3.13.12-alpine3.22 AS runtime
EXPOSE 8000
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY blog /app/blog
COPY manage.py /app
COPY ibira /app/ibira
COPY scripts /app/scripts
COPY global /app/global
COPY .env /app/.env

ENTRYPOINT ["/app/.venv/bin/python"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]