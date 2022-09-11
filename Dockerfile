# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker


RUN pip install requests flask flask_restful pandas flask_cors statsmodels sklearn numpy

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]



