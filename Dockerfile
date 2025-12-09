ARG DOCKER_REPO_URL=docker.io
ARG BASE_IMAGE=python
ARG BASE_TAG=3.12-slim

FROM ${DOCKER_REPO_URL}/${BASE_IMAGE}:${BASE_TAG} AS app

ARG ENVIRONMENT=production

USER root

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/appuser/.local/bin:${PATH}"

WORKDIR /app

COPY requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/${ENVIRONMENT}.txt

COPY --chown=appuser:appuser . .

RUN adduser --disabled-password --gecos "" appuser && \
    chmod +x /app/entrypoint.py && \
    chown -R appuser:appuser /app

HEALTHCHECK --interval=30s --timeout=10s \
    CMD python -c "print('healthy')" || exit 1

USER appuser

CMD ["python", "/app/entrypoint.py"]
