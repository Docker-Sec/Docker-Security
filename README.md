# INSE 6130 - Docker Security

Private repo to share resources, ideas and plans for INSE6130 Docker Security Project.

#### Team Members:

##### Attackers:

1. Mohit Balu 
2. Bikramjeet Singh
3. Nithya Sri Bommakanti
4. Harpreet Kaur

##### Defenders:

5. Milanpreet Kaur
6. Gouresh Chauhan
7. Rabiatou Oubbo Modi
8. Srividya Poshala

--------------------------------------

#### Attack Scenario 1:

![Attack1](https://user-images.githubusercontent.com/30471250/155872803-dde39599-1413-49c2-9a9c-818964e37d61.jpg)


#### Defense for Attack Scenario 1 (Tentative):

1. Implement python script to detect (and generate alert) if any of the sensitive information (such as PASS, KEY, APIKEY, TOKEN) is being disclosed in manifest file of the images on the docker registry.
2. Implement python script to detect (and generate alert) if any of the running docker containers is mounting docker.sock socket file.
3. Implement python script to detect (and generate alert) if any of the docker containers is running with unnecessary capabilities which can be abused by an adversary.
4. Implement a python script to generate alert when someone logins via SSH to docker container from unidentified IP address. (Bonus)

#### Attack Scenario 2

TBD

--------------------------------------

#### Resources:

links.txt : URLs for docker security articles, medium blogs and guides.

--------------------------------------

#### Attack Scenario Real World Context:

![image](https://user-images.githubusercontent.com/30471250/155866025-f3f907a8-41c7-499a-b84e-4b3eba46289b.png)
Source: https://devopscube.com/run-docker-in-docker/
