### Building Attack Scenario for Attack 1
---

1. Install and run Docker environment on the system and start docker registry service (Refer to useful commands)

2. Have a look at ./Dockerfiles/C[1,2]/Dockerfile to understand structure of the Dockerfile

2. Create Image linux:C1 (for container C1) from Dockerfile and push it to the registry. Navigate to ./Dockerfiles/C1/ and run following commands

        sudo docker build -t app-frontend:latest .
        sudo docker tag app-frontend:latest localhost:5000/app-frontend:latest
        sudo docker push localhost:5000/app-frontend:latest
		
		
3. Similarly, create Image linux:C2 (for container C2) from Dockerfile and push it to the registry. Navigate to ./Dockerfiles/C2 and run following commands

        sudo docker build -t app-backend:latest .
        sudo docker tag app-backend:latest localhost:5000/app-backend:latest
        sudo docker push localhost:5000/app-backend:latest
		
		
4. Since the images are push onto the registry, the local copies of images can be deleted.

        sudo docker image rm app-frontend:latest
        sudo docker image rm localhost:5000/app-frontend:latest
        sudo docker image rm app-backend:latest
        sudo docker image rm localhost:5000/app-backend:latest
	
5. Pull the images from registry (real world scenario)

        sudo docker pull localhost:5000/app-frontend:latest	
        sudo docker pull localhost:5000/app-backend:latest
	
6. Now, start the container C1 with port 22 open and docker.sock socket mounted.
	
	sudo docker run -it -d -p 22:22 -v /var/run/docker.sock:/var/run/docker.sock app-frontend:latest
	
7. Also, start the container C2 **without privilege flag** but with SYS_ADMIN capability and apparmor disabled.

	sudo docker run --rm -it -d --cap-add=SYS_ADMIN --security-opt apparmor=unconfined app-backend:latest bash
	
*Stage for performing Attack1 is ready now. Navigate to StepsToReproduceAttack1.md*

#### References:

1. https://docs.docker.com/desktop/


---
