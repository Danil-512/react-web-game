Added work with Docker. The ability to connect from external addresses (in the local network and in the public network) is configured. 
Commands for initial setup and launch in the node: 
	npm i
	npm run dev
Commands for creating a Docker image and launching a container:
	docker build . -t nodeproject
	docker run --name react -p 5173:5173 nodeproject