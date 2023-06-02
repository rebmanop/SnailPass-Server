FROM python:3.10-slim
RUN apt-get update
RUN mkdir /snailpass-server
WORKDIR /snailpass-server
COPY ./requirements.txt /snailpass-server
RUN pip install -r requirements.txt
COPY . /snailpass-server
EXPOSE 5000
