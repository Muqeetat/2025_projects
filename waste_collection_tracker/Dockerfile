# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.4
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user for security
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy dependency file and install requirements
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy the entire project source code
COPY . .

# Ensure the non-root user can access project files
RUN chown -R appuser:appuser /app

# Switch to the non-privileged user
USER appuser

# Expose application port
EXPOSE 8000

# Ensure Python finds the application code
ENV PYTHONPATH=/app

# Start the FastAPI app
# CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
