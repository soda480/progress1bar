#   -*- coding: utf-8 -*-
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /progress1bar

COPY . /progress1bar/

RUN pip install pybuilder names
RUN pyb install_dependencies
RUN pyb install
