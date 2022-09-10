#Dockerfile, Image, Container

FROM python:3.8

ADD main.py .3
RUN pip install requests flask flask_restful pickle pandas flask_cors

CMD ["python", ".main.py"]