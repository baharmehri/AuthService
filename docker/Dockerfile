# syntax=docker/dockerfile:1
FROM python:3.12
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY ./requirements/requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install --upgrade setuptools
RUN pip install --upgrade  six
COPY . /code/