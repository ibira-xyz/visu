FROM public.ecr.aws/lambda/python:3.13.2025.09.30.13-x86_64

# Copy uv from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files
COPY pyproject.toml ${LAMBDA_TASK_ROOT}/pyproject.toml
COPY uv.lock ${LAMBDA_TASK_ROOT}/uv.lock

# Install dependencies
WORKDIR ${LAMBDA_TASK_ROOT}
RUN uv sync

# Copy application files
COPY templates/ ${LAMBDA_TASK_ROOT}/templates/
COPY main.py ${LAMBDA_TASK_ROOT}/main.py

# Set environment variable to indicate Docker environment
ENV CDN_BASE_URL='https://cdn.ibira.xyz'
ENV PYTHONPATH="${LAMBDA_TASK_ROOT}:${LAMBDA_TASK_ROOT}/.venv/lib/python3.13/site-packages"

# Set the CMD to your handler
CMD ["main.lambda_handler"]