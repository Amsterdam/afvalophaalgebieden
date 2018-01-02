FROM amsterdam/python:latest
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN apt-get install -y libgeos-dev netcat \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
	&& adduser --system datapunt \
	&& pip3 install uwsgi

WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

USER datapunt
COPY afvalophaalgebieden /app/
COPY .jenkins-import /.jenkins-import/
CMD ["/app/docker-run.sh"]

