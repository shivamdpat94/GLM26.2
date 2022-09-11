

# start by pulling the python image
FROM python:3.8

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install requests flask flask_restful pandas flask_cors statsmodels sklearn numpy

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["main.py" ]