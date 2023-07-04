FROM python:3.11
LABEL authors="Opstree Solutions" \
      application="Attendance API" \
      version="v0.1.0"

WORKDIR /api

RUN pip3 install poetry gunicorn

COPY pyproject.toml poetry.lock .
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

COPY client/ client/
COPY models/ models/
COPY router/ router/
COPY utils/ utils/
COPY app.py app.py
COPY log.conf log.conf

ENTRYPOINT ["gunicorn"]

CMD [ "app:app", "--log-config", \
    "log.conf", "-b", "0.0.0.0:8080"]
