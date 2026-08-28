FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir '.[api]'

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "python -m uvicorn hdmatch.api.relationship_pilot_app:app --host 0.0.0.0 --port ${PORT:-8000}"]
