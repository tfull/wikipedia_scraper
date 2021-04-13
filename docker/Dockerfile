FROM python:3.8

RUN useradd -m tester

COPY ./wscraper /resource/wscraper
COPY ./setup.py /resource/setup.py
COPY ./README.md /resource/README.md

WORKDIR /resource

RUN python setup.py install

RUN pip install mecab-python mysqlclient unidic-lite

COPY --chown=tester:tester ./docker/run.sh /home/tester/run.sh
