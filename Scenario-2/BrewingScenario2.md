### Building Attack Scenario for Attack 2
---

#### Pre-requisites:

1. Ubuntu OS < 20.04
2. Docker Engine < 18.09.2
3. runc <= 1.0-rc6

As mentioned in https://www.cvedetails.com/cve/CVE-2019-5736/ 
>runc through 1.0-rc6, as used in Docker before 18.09.2 and other products, allows attackers to overwrite the host runc binary (and consequently obtain host root access) by leveraging the ability to execute a command as root within one of these types of containers: (1) a new container with an attacker-controlled image, or (2) an existing container, to which the attacker previously had write access, that can be attached with docker exec. This occurs because of file-descriptor mishandling, related to /proc/self/exe.
	
#### Steps:

1. Install and run Docker environment as per following steps:

    a. Spin up Ubuntu Bionic Beaver VM (18.04), as the docker version vulnerable to runC exploit is compatible with this version of Ubuntu.
  
    b. Run following for setting up docker environment:
	
        sudo apt-get remove docker docker-engine docker.io containerd runc
        sudo apt-get update
        sudo apt-get install ca-certificates curl gnupg lsb-release
        sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
        sudo echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        sudo apt-get update
  
     c. Now, install docker-ce version 18.09.0~3-0~ubuntu-bionic by running following command. This will install Docker Engine v18.09.0
	
        sudo apt install docker-ce=5:18.09.0~3-0~ubuntu-bionic
		
	Available docker-ce versions can be listed with sudo apt-cache madison docker-ce
	
    d. Now, download and install Docker Client v18.09.0 and runc v1.0.0 with following commands:
	
        sudo wget https://download.docker.com/linux/ubuntu/dists/bionic/pool/stable/amd64/docker-ce-cli_18.09.0~3-0~ubuntu-bionic_amd64.deb
        sudo wget https://download.docker.com/linux/ubuntu/dists/bionic/pool/stable/amd64/containerd.io_1.2.0-1_amd64.deb
        sudo dpkg -i docker-ce-cli_18.09.0~3-0~ubuntu-bionic_amd64.deb
        sudo dpkg -i containerd.io_1.2.0-1_amd64.deb

    e. Installed versions can be checked with following commands:
	
       sudo docker version #for Docker client and Docker Engine
       sudo runc -v

2. Start docker registry service and host two docker images (an app-server and a database) of a web-application that prints credit score when certain inputs are provided. Start the container for both of the images. The web application with an interface and a database (containing credit information) is up and running now.  **[To be implemented...]**

---

#### References:

1. https://www.cvedetails.com/cve/CVE-2019-5736/
2. https://unit42.paloaltonetworks.com/breaking-docker-via-runc-explaining-cve-2019-5736/

