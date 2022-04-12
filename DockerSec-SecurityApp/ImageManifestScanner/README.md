1. Install following dependencies

	sudo apt install -y python3-pip
	sudo pip install docker
	sudo pip install docker_registry_client
	sudo pip install sh
	cd gittyleaks
	python3 setup.py install

2. Then run the script, it will fetch the data from docker registry running on your system.

	sudo python3 scanImageManifest.py
