import os
import docker 
client = docker.from_env()
containers = client.containers.list()

#print(containers)

print("\33[33m\n\n-------------------------------------------------------------------------------\n\t\tDockerSec : Docker Socket Detector\n-------------------------------------------------------------------------------")

detected = list()

for each in containers:

  container = str(each)[12:-1]

  print("\33[37m"+"\n*[Finding docker socket in container: "+container+"]...")

  result = each.exec_run("find / -name docker.sock")
  #print(result)

  if("docker.sock" in str(result)):
    detected.append(container)

if(len(detected)>0):
  print("\n"+"\33[31m"+"[Result] :: Docker socket is found mounted inside the following running containers:\n"+"\33[37m")
  print("\33[1m\n-------------------------------------------------------------------")
  print("\33[1m"+"Container ID\t:\tImage Name")
  print("\33[1m-------------------------------------------------------------------\n")

  for each in detected:
    imagename = str(os.popen("docker inspect --format='{{.Config.Image}}' "+each).read())
    print("\33[1m"+"123"+each+"\t:\t"+imagename[:-1])

else:
  print("\n"+"\33[32m"+"[Result] :: Docker socket is not mounted in any of the running containers.\n")

print("\n\n")