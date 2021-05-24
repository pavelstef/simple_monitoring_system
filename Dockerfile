# Simple Monotoring System docker file

# Base
FROM python:3.8-slim

# Commands
RUN apt-get update && apt-get install -y iputils-ping
RUN mkdir -p /opt/sms_app/
WORKDIR /opt/sms_app/
COPY . /opt/sms_app/
RUN pip3 install pip --upgrade && pip install --no-cache-dir -r requirements.txt
RUN chmod a+x ./run.sh

# Ports
EXPOSE 8001