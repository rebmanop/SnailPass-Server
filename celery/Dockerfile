FROM python:3.10-slim

RUN mkdir /snailpass-server
WORKDIR /snailpass-server
COPY .. /snailpass-server

RUN apt-get update && apt-get install -y \
    build-essential # python-dev libssl-dev openssl


RUN pip3 install -r ../requirements-prod.txt

CMD ["celery", "-A", "celery_app.celery", "worker" "--loglevel=info"]