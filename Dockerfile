ARG DJANGO_CONTAINER_VERSION=1.4.0
FROM gcr.io/uwit-mci-axdd/django-container:${DJANGO_CONTAINER_VERSION} as app-container

USER root
RUN apt-get install -y git-crypt && apt-get install gnupg
USER acait

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ /app/project/
RUN /app/bin/pip install -r requirements.txt

#RUN . /app/bin/activate && python manage.py test
FROM gcr.io/uwit-mci-axdd/django-test-container:${DJANGO_CONTAINER_VERSION} as app-test-container

COPY --from=app-container /app/ /app/
