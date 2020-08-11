FROM acait/django-container:1.0.39 as app-container

USER root
RUN apt-get update && apt-get install mysql-client libmysqlclient-dev -y
USER acait

ADD --chown=acait:acait accountsynchr/VERSION /app/accountsynchr/
ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/
RUN . /app/bin/activate && pip install -r requirements.txt

RUN . /app/bin/activate && pip install mysqlclient

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ project/

#RUN . /app/bin/activate && python manage.py test

FROM acait/django-test-container:1.0.36 as app-test-container

COPY --from=0 /app/ /app/
COPY --from=0 /static/ /static/
