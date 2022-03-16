## INSE6130 - Docker Security Project : Steps to Reproduce for Attack 2

* A. Build a malicious image similar to app-server but with runC exploit embedded into it.
* B. Push image to docker registry and compromise the 'app-server' container and hence the host OS.
* C. Access the 'database' container and exfiltrate sensitive data. **\[Goal\]**

![Attack2](https://user-images.githubusercontent.com/30471250/158512857-d7dcb6d1-7992-4ba0-907e-d125504d07d9.jpg)

---

#### A. Build a malicious image similar to app-server but with runC exploit embedded into it.


#### Context:

*A Docker environment is running which hosts a web application containing credit card information of multiple users. The docker environment hosts two containers 'app-server' and 'database' AND an unprotected registry service. As an attacker our goal is to find a way into the environment and steal credit card information residing in the 'database' container. The 'database' container is not exposed to the external world as it only communicates with the app-server inside the environment using docker0 bridge. The app-server is exposed outside the docker environment on eth0 interface since it is meant to be accessed by the users of the application.*

#### Steps:

Create a malicious image with runC exploit and explain the code (Refer https://github.com/twistlock/RunC-CVE-2019-5736)

**[To be implented and steps to be explained...]**

---

#### B. Comprimising Container C2:

#### Background: 

*Malicious image of app-server with runC exploit has been built. As an attacker this image can be pushed into unprotected docker registry with latest tag. When a legitimate user of the system will run app-server container, the docker engine will pull the latest (and unknowingly malicious) image from the registry and start the container. The runC exploit will execute and land the attacker with the reverse shell from the underlying operating system*

#### Steps:

Push the image into the registry and re-start the container as a legitimate user. 
runC exploit will execute and attacker will get access to host OS.

**[To be implented and steps to be explained...]**


-----

#### C. Comprimising Underlying OS:

#### Steps:

Since the attacker has access to host OS, S(he) can easily read information for 'database' container and exfiltrates sensitive information.

**[To be implented and steps to be explained...]**

---

#### References:

1. https://github.com/twistlock/RunC-CVE-2019-5736	[runC exploit written in C]
2.

#### Challenges Faced:

1. As an attacker outside the docker environment, other than compromising through an explicitely installed application, there are only few ways to do  initial compromise of the environment (e.g. through docker registry or thorugh exposed docker API). We struggled to figure out such vulnerability in docker components, which would let us do initial compromise of the environment and also further allow us to pivot to other containers or to perform docker escape.
      
      Compromising initially by uploading malicious image would have given us the access to the container itself however escaping from that container would have been very difficult, unless the container is intentionally run with some potential misconfiguration by a legitimate user, which is a least likely scenario in the real world.
      
      Similarly, to implement docker escape scenario, we would have required access to an already running container with some misconfiguration, which was possible by compromising some explicitely installed application on the docker container.
      
      In the end, we figured out that an attacker outside the docker environment can do initial compromise by pushing malicious image (with runC exploit) into an unprotected docker registry and at the same time perform docker escape through runC exploit and get access to the host OS.

2. While implementing runC exploit, we faced issues to figure out the exact versions of Ubuntu OS, Docker engine and runc that are compatible with each other and also fulfils the requirements to perform runC exploit. We approached through trial and error method and tried installing and running different versions until we came up with working ones (which are Ubuntu OS v18.04, Docker Engine v18.09.0~3~0 and runc v1.0.0-rc5)
