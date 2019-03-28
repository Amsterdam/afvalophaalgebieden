FROM amsterdam/python
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

ARG https_proxy=http://10.240.2.1:8080/
ENV https_proxy=$https_proxy

WORKDIR /app/
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY afvalophaalgebieden /app/
COPY .jenkins-import /.jenkins-import/

USER datapunt

CMD ["/app/docker-run.sh"]
