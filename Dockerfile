FROM amsterdam/python3.6
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN rm -rf /data
RUN mkdir /data && chown datapunt /data

WORKDIR /app/
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY afvalophaalgebieden /app/
COPY .jenkins-import /.jenkins-import/

USER datapunt

CMD ["/app/docker-run.sh"]
