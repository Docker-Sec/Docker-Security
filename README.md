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

![AttackScenario1](https://user-images.githubusercontent.com/30471250/155865630-4d68e9a3-95ed-4976-b0f8-70b7a99aa90e.jpg)

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


