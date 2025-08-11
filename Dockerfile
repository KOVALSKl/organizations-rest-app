FROM python:3.11.4-slim-buster

ARG UID
ARG GID

RUN groupadd -g "$GID" appgroup \
    && useradd --uid "$UID" --gid "$GID" --create-home --no-log-init appuser

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN chown -R appuser:appgroup /app

USER appuser

CMD ["uvicorn", "--reload", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]