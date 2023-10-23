ARG DJANGO_CONTAINER_VERSION=1.4.1
FROM us-docker.pkg.dev/uwit-mci-axdd/containers/django-container:${DJANGO_CONTAINER_VERSION} as app-container

USER root
RUN apt-get update && apt-get install libpq-dev -y
RUN apt-get update && apt-get install postgresql-client -y

RUN mkdir /data
USER acait

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ /app/project/

RUN /app/bin/pip install -r requirements.txt
RUN /app/bin/pip install psycopg2

#RUN . /app/bin/activate && python manage.py test
FROM us-docker.pkg.dev/uwit-mci-axdd/containers/django-test-container:${DJANGO_CONTAINER_VERSION} as app-test-container

COPY --from=app-container /app/ /app/
COPY --from=app-container /data/ /data/
