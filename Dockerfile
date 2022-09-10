#Dockerfile, Image, Container

FROM python:3.8
WORKDIR /app
COPY . .


RUN pip install requests flask flask_restful pandas flask_cors statsmodels sklearn numpy
ENTRYPOINT ["python"]
CMD ["main.py"]


