FROM acait/django-container:1.1.7 as app-container

USER root
RUN apt-get install -y git-crypt && apt-get install gnupg
USER acait

ADD --chown=acait:acait accountsynchr/VERSION /app/accountsynchr/
ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/
RUN . /app/bin/activate && pip install -r requirements.txt

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ project/
ADD --chown=acait:acait docker/management_command.sh /scripts/
RUN chmod u+x /scripts/management_command.sh

RUN . /app/bin/activate && python manage.py test

FROM acait/django-test-container:1.1.7 as app-test-container

COPY --from=app-container /app/ /app/
