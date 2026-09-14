ARG DJANGO_CONTAINER_VERSION=3.1.4

FROM us-docker.pkg.dev/uwit-mci-axdd/containers/django-container:${DJANGO_CONTAINER_VERSION} AS app-container

USER root
RUN mkdir /data
USER acait

COPY --chown=acait:acait . /app/
COPY --chown=acait:acait docker/ /app/project/

RUN /app/bin/pip install -r requirements.txt

#RUN . /app/bin/activate && python manage.py test
FROM us-docker.pkg.dev/uwit-mci-axdd/containers/django-test-container:${DJANGO_CONTAINER_VERSION} AS app-test-container

COPY --from=app-container /app/ /app/
COPY --from=app-container /data/ /data/
