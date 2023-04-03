FROM python:3.11-slim-bullseye AS compile-image

RUN apt-get update && apt-get install -y libpq-dev libev-dev gcc

RUN pip install --user --upgrade pip
RUN pip install --user --upgrade setuptools wheel
COPY ./requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim-bullseye AS build-image

RUN apt-get update && apt-get install -y libpq5
RUN useradd --create-home appuser

COPY --from=compile-image /root/.local /home/appuser/.local

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /home/appuser/
RUN mkdir -p /app /log
USER appuser
WORKDIR /home/appuser/app

CMD while ! python3 manage.py sqlflush > /dev/null 2>&1 ; do sleep 1 ; done && \
    python3 manage.py createdatabase_if_not_exist && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    python3 manage.py createsuperuser_if_not_exist \
    --user=${DJANGO_SUPERUSER_NAME} \
    --password=${DJANGO_SUPERUSER_PASS} \
    --email=${DJANGO_SUPERUSER_EMAIL}; \
    gunicorn --worker-tmp-dir /dev/shm \
    --workers=${GUNICORN_WORKERS} \
    --bind 0.0.0.0:8000 \
    --log-level warning --log-file /home/appuser/log/gunicorn-error.log \
    core.wsgi:application