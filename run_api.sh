#!/bin/sh

echo 1-Container             2-Cluster?
read option

if [ $option -eq 1 ]
then
################  ONLY NEEDED TO RUN ONCE. CAN BE REMOVED ONCE IMAGE IS ON DEVICE ##############
        docker pull shivamdpat94/dockerhub:myfirstimagepush
################################################################################################
        docker run -d -p 5000:5000 shivamdpat94/dockerhub:myfirstimagepush
fi







if [ $option -eq 2 ]
then
################  ONLY NEEDED TO RUN ONCE. CAN BE REMOVED ONCE IMAGE IS ON DEVICE ##############
        docker pull shivamdpat94/dockerhub:myfirstimagepush
################################################################################################
        minikube start

################  ONLY NEEDED TO RUN ONCE. CAN BE REMOVED ONCE IMAGE IS ON DEVICE
        minikube image load shivamdpat94/dockerhub:myfirstimagepush
################################################################################################
	      kubectl apply -f deployment.yaml
	      minikube service flask-test-service

fi