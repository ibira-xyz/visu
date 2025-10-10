# Dockerfile for individual Lambda functions
# Usage: docker buildx build \
#          -f Dockerfile.lambda \
#          --build-arg LAMBDA_FILE=lambda_home.py \
#          --build-arg STAGE=dev \
#          --platform linux/amd64 \
#          --provenance=false \
#          -t docker-image:dev .

FROM public.ecr.aws/lambda/python:3.13.2025.09.30.13-x86_64

# Build argument for which lambda file to use
ARG LAMBDA_FILE=lambda_home.py
ARG STAGE=dev

# Copy uv from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files
COPY pyproject.toml ${LAMBDA_TASK_ROOT}/pyproject.toml
COPY uv.lock ${LAMBDA_TASK_ROOT}/uv.lock

# Install dependencies
WORKDIR ${LAMBDA_TASK_ROOT}
RUN uv sync --no-dev

# Copy application files
COPY templates/ ${LAMBDA_TASK_ROOT}/templates/
COPY renderers/ ${LAMBDA_TASK_ROOT}/renderers/
COPY config/${STAGE}.yaml ${LAMBDA_TASK_ROOT}/config.yaml
COPY ${LAMBDA_FILE} ${LAMBDA_TASK_ROOT}/lambda_handler.py

# Set environment variable to indicate Docker environment
ENV PYTHONPATH="${LAMBDA_TASK_ROOT}:${LAMBDA_TASK_ROOT}/.venv/lib/python3.13/site-packages"

# Set the CMD to the handler
CMD ["lambda_handler.handler"]