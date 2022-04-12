import docker
from docker_registry_client import DockerRegistryClient, Repository, Image
from docker_registry_client._BaseClient import BaseClientV1, BaseClientV2
import json
import re
import ast
from sh import grep, cat
import requests
import subprocess 
import os


print("\n\n-------------------------------------------------------------------------------\n\t\tDockerSec : Image Manifest Scanner\n-------------------------------------------------------------------------------")

url = "http://localhost:5000/"
client = DockerRegistryClient(url)

#print(client.repositories())
#print(client.repository("app-frontend"))
#print(client.api_version)
client.refresh()

#print(list(client.repositories().keys()))

images = list(client.repositories().keys())


for image in images:

#image="app-frontend"

	print("\n+[Scanning image '"+image+"']\n")


	rep = Repository(BaseClientV2(url), image)
	#print(rep.tags())

	tag = rep.tags()[0]

	content = rep.manifest(tag)[0]
	#print(content)
	manif = eval(str(content))
	#print(manif)
	#print(manif["history"])

	f = open("newfile.txt","w")
	f.write(str(manif))
	f.close()

	f = open("his.txt","w")
	f.write(str(manif["history"]))
	f.close()

	#print(len(manif["history"]))
	#print(manif["history"][1])


	"""
	for each in manif["history"]:
	print(str(each)+"\n")
	grep('-i','-e',"secret", str(each))	#detect here

	"""

	json_url = "https://jsonformatter.curiousconcept.com/process"
	data = {'data':str(manif["history"]), 'process': 'true', 'jsontemplate':'1', 'jsonspec':'4', 'jsonfix':'on', 'version':'2'}

	#print(data)

	r = requests.post(json_url, data, verify=False)


	f = open("response.txt","w")
	f.write(r.text)
	f.close()
	#print(r.text)

	os.system("mkdir files && cd files && git init >/dev/null 2>&1 && git config --global user.name 'testDockerSecurity' && git config --global user.email 'test@dockersecurity.com'")

	cmd = "cat response.txt | jq . > files/"+str(image+"["+tag+"]")

	os.system(cmd)

	#os.system("cat filteredresponse.txt")

	os.system("cd files && git add . >/dev/null 2>&1 && git commit -m 'INSE6130' >/dev/null 2>&1")

	os.system("cd files && sudo gittyleaks -o -b ")

	os.system("rm -rf ./files")

