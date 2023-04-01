FROM python:3.10-slim
RUN apt-get update
RUN mkdir /snailpass-server
WORKDIR /snailpass-server
COPY . /snailpass-server
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
