#!/bin/sh
## Ask the user for their name
echo 1-Container             2-Cluster?
read option

if [ $option -eq 1 ]
then
        docker build --tag python-docker .
        docker run -d -p 5000:5000 python-docker
fi
if [ $option -eq 2 ]
then
        docker build --tag python-docker .
        minikube start
	      kubectl apply -f deployment.yaml
	      minikube service flask-test-service

fi