FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

COPY pyproject.toml uv.lock ./

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    libxml2 \
    libxslt1.1 \
    curl && \
    BUILD_PKGS="gcc libxml2-dev libxslt-dev python3-dev" && \
    apt-get install -y --no-install-recommends $BUILD_PKGS && \
    echo "Installing uv..." && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    echo "Installed uv version:" && \
    uv --version && \
    echo "Installing project and dependencies from pyproject.toml (using uv.lock)..." && \
    uv pip install --system --no-cache . && \
    apt-get purge -y --auto-remove $BUILD_PKGS curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]