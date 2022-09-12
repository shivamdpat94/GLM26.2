# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
RUN mkdir /app
WORKDIR /app/
ADD . /app/

RUN pip install -r requirements.txt
CMD ["python", "/app/app.py"]



