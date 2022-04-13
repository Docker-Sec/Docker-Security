import docker 
import os
import subprocess
client = docker.from_env()
containers = client.containers.list()


for each in containers:

  container = str(each)[12:-1]

  print("\33[96m"+"\n*[Finding capabilities in container: "+container+"]...\n")
  result = each.exec_run("capsh --print")[1]
  result = result.decode('utf-8')
  print("\33[1m-------------------------------------------------------------------")
  print("\33[1m"+result)

  cap_list=['cap_sys_admin','cap_sys_ptrace','cap_sys_module','cap_dac_read_search','cap_dac_override']

  for element in cap_list:
    if element in result:
      print("Container "+ container +" has abusable capability '"+element+"'")

      val1 = input("Do you want to remove this capability? [y/n]: ")
       
      if val1 == "Y" or val1 =="y":
        #print("value of id " + container)
        imageid = os.popen("docker inspect --format='{{.Config.Image}}' " + container).read()[:-1] # from container id will get image id store it in some variable
        #print("value of x1", output)
        #print("element", element)

        #print("value of x1[6:]",imageid)
        print("\n+[Restarting the container with removed capabilities]...\n")
        os.system("docker stop " + container)  # stop container id
        command = "docker run -itd --restart=always --cap-drop=" + "'" + element + "' " + imageid
        #print(command)
        os.system(command)  # remove capabilities
      else:
        print("Capabilities Saved")