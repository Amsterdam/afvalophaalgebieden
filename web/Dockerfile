FROM python:3
MAINTAINER datapunt.ois@amsterdam.nl

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN apt-get update \
	&& apt-get clean \
	&& apt-get install -y libgeos-dev \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
	&& adduser --system datapunt \
	&& mkdir -p /static \
	&& chown datapunt /static \
	&& pip install uwsgi

WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

USER datapunt
COPY afvalophaalgebieden /app/
CMD /app/docker-entrypoint.sh
