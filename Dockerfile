FROM python:3.10-slim
RUN apt-get update
RUN mkdir /snailpass-rest-api
WORKDIR /snailpass-rest-api
COPY . /snailpass-rest-api
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
