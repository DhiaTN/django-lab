FROM python:2.7
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /web/src
ADD . /web/src
WORKDIR /web/src
RUN pip install -r requirements.txt