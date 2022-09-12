#!/bin/sh

echo 1-Container             2-Cluster?
read option

if [ $option -eq 1 ]
then
################  ONLY NEEDED TO RUN ONCE. CAN BE REMOVED ONCE IMAGE IS ON DEVICE ##############
        docker build --tag python-docker .
################################################################################################
        docker run -d -p 5000:5000 python-docker
fi







if [ $option -eq 2 ]
then
################  ONLY NEEDED TO RUN ONCE. CAN BE REMOVED ONCE IMAGE IS ON DEVICE ##############
        docker build --tag python-docker .
################################################################################################
        minikube start

################  ONLY NEEDED TO RUN ONCE. CAN BE REMOVED ONCE IMAGE IS ON DEVICE ....Look into "minikube image load python-docker ."##############
        minikube image load python-docker
################################################################################################
	      kubectl apply -f deployment.yaml
	      minikube service flask-test-service

fi