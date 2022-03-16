#### Defense for Attack Scenario 1 (Tentative):

1. Implement python script to detect (and generate alert) if any of the sensitive information (such as PASS, KEY, APIKEY, TOKEN) is being disclosed in manifest file of the images on the docker registry. Also HTTP authentication for docker registry can be implemented to protect the registry service from being accessed by unauthenticated users.
2. Implement python script to detect (and generate alert) if any of the running docker containers is mounting docker.sock socket file.
3. Implement python script to detect (and generate alert) if any of the docker containers is running with unnecessary capabilities which can be abused by an adversary.
4. Implement a python script to generate alert when someone logins via SSH to docker container from unidentified IP address. (Bonus)
