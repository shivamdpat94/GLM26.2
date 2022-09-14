#!/bin/sh





#Requires Docker and Minikube


echo 1-Container             2-Cluster?
read option

if [ $option -eq 1 ]
then
################  ONLY NEEDED TO RUN ONCE. CAN BE REMOVED ONCE IMAGE IS ON DEVICE ##############
        docker pull shivamdpat94/dockerhub2:myfirstimagepush
################################################################################################
        docker run -d -p 5000:5000 shivamdpat94/dockerhub2:myfirstimagepush
fi







if [ $option -eq 2 ]
then

        minikube start

        eval $(minikube docker-env)

         git clone https://github.com/shivamdpat94/GLM26.2.git

         cd GLM26.2/


################  ONLY NEEDED TO RUN ONCE. CAN BE REMOVED ONCE IMAGE IS ON DEVICE ##############
        docker pull shivamdpat94/dockerhub2:myfirstimagepush
################################################################################################

	      kubectl apply -f deployment.yaml
	      minikube service flask-test-service

fi