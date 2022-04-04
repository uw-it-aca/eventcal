FROM gcr.io/uwit-mci-axdd/django-container:1.3.8 as app-container

USER root
RUN apt-get install -y git-crypt && apt-get install gnupg
USER acait

ADD --chown=acait:acait accountsynchr/VERSION /app/accountsynchr/
ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/
RUN . /app/bin/activate && pip install -r requirements.txt

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ project/

#RUN . /app/bin/activate && python manage.py test

FROM gcr.io/uwit-mci-axdd/django-test-container:1.3.8 as app-test-container

COPY --from=app-container /app/ /app/
