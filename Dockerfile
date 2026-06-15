# syntax=docker/dockerfile:1.7
# ─────────────────────────────────────────────────────────────────────────────
# ishar-web — Django + Channels (Daphne) container.
#
# Single-stage build. Wheels exist for cryptography/cffi/PyNaCl on common
# platforms, but we keep gcc + dev headers around in case pip falls back to
# source. The image is ~300MB; acceptable for a small Lightsail box.
#
# Run:    daphne serves both HTTP and WebSocket on :8000 inside the container.
# Front:  nginx on the host reverse-proxies to 127.0.0.1:8000.
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Build + runtime deps. Most Python packages here have prebuilt wheels for
# linux/amd64; the build-essential layer is insurance for arm64 / edge cases.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        libffi-dev \
        libssl-dev \
        netcat-openbsd \
        tini \
    && rm -rf /var/lib/apt/lists/*

# Non-root user. UID/GID matches what nginx-on-host would expect if the static
# dir is shared via bind-mount.
RUN groupadd --system --gid 1000 ishar \
    && useradd  --system --gid 1000 --uid 1000 --home-dir /app --shell /bin/bash ishar

WORKDIR /app

# Install deps first for better caching.
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the application.
COPY --chown=ishar:ishar . /app

# Pre-create writable directories the app expects at runtime. Volumes mount
# over these in compose; empty seed is fine.
RUN install -d -o ishar -g ishar /app/cache /app/logs /app/static /app/media

USER ishar

# Daphne port. Host nginx talks to 127.0.0.1:8000.
EXPOSE 8000

ENTRYPOINT ["/usr/bin/tini", "--"]

# Daphne serves both HTTP and WebSocket via asgi.application.
# DJANGO_SETTINGS_MODULE is set in the environment via the compose file.
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "--proxy-headers", "asgi:application"]
