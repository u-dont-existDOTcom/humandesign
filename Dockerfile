FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir '.[api]'

ENV PYTHONUNBUFFERED=1

CMD ["/bin/sh", "-c", "exec python -m uvicorn hdmatch.api.relationship_llm_jsonmode_app:create_relationship_llm_jsonmode_app_from_env --factory --host 0.0.0.0 --port ${PORT:-8000}"]
