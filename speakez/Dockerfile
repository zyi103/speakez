FROM python:3

WORKDIR /var/webapp

COPY requirements.txt /var/webapp/requirements.txt

RUN pip install -r /var/webapp/requirements.txt

COPY uwsgi.ini /var/webapp/uwsgi.ini

RUN pip install uwsgi

COPY . /var/webapp

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 9000
EXPOSE 9001
EXPOSE 3000

CMD [ "entrypoint.sh" ]