### Building Attack Scenario for Attack 1
---

1. Install and run Docker environment on the system and start docker registry service (Refer to useful commands)

2. Have a look at ./Images/C[1,2]/Dockerfile to understand structure of the Dockerfile

2. Create Image linux:C1 (for container C1) from Dockerfile and push it to the registry. Navigate to Images/C1/ and run following commands

        sudo docker build -t linux:C1
        sudo docker tag ubuntu:C1 localhost:5000/linux:C1
        sudo docker push localhost:5000/linux:C1
		
		
3. Similarly, create Image linux:C2 (for container C2) from Dockerfile and push it to the registry. Navigate to Images/C2 and run following commands

        sudo docker build -t linux:C2
        sudo docker tag ubuntu:C1 localhost:5000/linux:C2
        sudo docker push localhost:5000/linux:C2
		
		
4. Since the images are push onto the registry, the local copies of images can be deleted.

        sudo docker image rm linux:C1
        sudo docker image rm localhost:5000/linux:C1
        sudo docker image rm linux:C2
        sudo docker image rm localhost:5000/linux:C2
	
5. Pull the images from registry (real world scenario)

        sudo docker pull localhost:5000/linux:C1	
        sudo docker pull localhost:5000/linux:C2
	
6. Now, start the container C1 with port 22 open and docker.sock socker mounted.

	      sudo docker run -it -d -p 22:22 -v /var/run/docker.sock:/var/run/docker.sock linux:C1
	
7. Also, start the container C2 without privilege flag but with SYS_ADMIN capability and apparmor disabled.

	      sudo docker run --rm -it -d --cap-add=SYS_ADMIN --security-opt apparmor=unconfined linux:C2 bash
	
*Stage for performing Attack1 is ready now. Navigate to StepsToReproduceAttack1.md*
