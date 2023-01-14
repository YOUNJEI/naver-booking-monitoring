FROM python:3.8-alpine
MAINTAINER kyj951211@gmail.com
WORKDIR /usr/src/app

COPY src src
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED = 1
ENV NAVER_ACC_KEY=secret
ENV NAVER_PHONE_NUMBER_FROM=secret
ENV NAVER_SECRET_KEY=secret
ENV NAVER_SVC_ID=secret
ENV MY_PHONE_NUMBER=secret

ENTRYPOINT python3 src/main.py