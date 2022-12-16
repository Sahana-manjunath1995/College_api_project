FROM python:3.8


WORKDIR /home

RUN apt update -y && apt install vim -y
COPY requirements.txt  /home/
RUN pip  install -r requirements.txt

