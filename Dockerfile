FROM amsterdam/python:3.8-buster AS builder
MAINTAINER datapunt@amsterdam.nl

COPY requirements* ./
ARG PIP_REQUIREMENTS=requirements.txt
RUN pip install --no-cache-dir -r $PIP_REQUIREMENTS

# Start runtime image
FROM amsterdam/python:3.8-slim-buster

# Copy python build artifacts from builder image
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/

WORKDIR /app
RUN mkdir /data && chown datapunt /data

COPY afvalophaalgebieden /app/
COPY .jenkins-import /.jenkins-import/

EXPOSE 8000
USER datapunt
CMD ["/app/docker-run.sh"]
