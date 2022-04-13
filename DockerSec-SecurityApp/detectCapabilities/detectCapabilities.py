import docker 
import os
import subprocess
client = docker.from_env()
containers = client.containers.list()

print("\33[33m\n\n-------------------------------------------------------------------------------\n\t\tDockerSec : Capability Finder\n-------------------------------------------------------------------------------")


for each in containers:

  container = str(each)[12:-1]
  imageid = os.popen("docker inspect --format='{{.Config.Image}}' " + container).read()[:-1] # Image name from container ID

  print("\33[96m"+"\n\n* [Finding capabilities in container: "+container+" ("+imageid+")]")
  print("-------------------------------------------------------------------------------------")
  result = each.exec_run("capsh --print")[1]
  result = result.decode('utf-8')
  
  if "unknown" in result:
    print("\n\33[33m* [Not applicable to this container]")
    pass
  else:
    print("\33[0m"+result)


  cap_list=['cap_sys_admin','cap_sys_ptrace','cap_sys_module','cap_dac_read_search','cap_dac_override']

  found = False
  to_be_removed=[]
  to_be_kept=[]
  hasremovable = False

  for element in cap_list:
    if element in result:
      found = True
      print("\33[31m- [Container "+ container +" ("+imageid+")"+" has abusable capability '"+element+"']")

      val1 = input("\33[0mIt is advised to drop the capability unless required. Would you like to remove this capability? [y/n]: ")
       
      if val1 == "Y" or val1 =="y":
        hasremovable = True
        to_be_removed.append(element)

        
      elif val1 == "N" or val1 == "n":
        to_be_kept.append(element)
        print("here="+element)
        print("\n\33[33mSkipping...")

  if(found and hasremovable):
    rem = ""
    for each in to_be_removed:
      rem+="--cap-drop="+each+" "
    #print("rem="+rem)

    kept = ""
    for each in to_be_kept:
      kept+="--cap-add="+each+" "
    #print("kept="+kept)

    print("\n\33[33m+ [Restarting the container with removed/retained capabilities]...\n")
    command = "sudo docker stop " + container
    print(command)
    os.system(command)  # stop container id

    command = "sudo docker run -itd --restart=always "+ rem +" "+kept+" "+imageid
    print(command)

    os.system(command)  # remove capabilities

  if(not found):
      print("\33[32m+ [Container "+ container +" ("+imageid+")"+" does not possess any abusable capability]")

print("\n\n")