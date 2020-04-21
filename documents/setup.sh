#!/usr/bin/env bash
# Creating a new network for my webserver container and my mysql database container
docker network create my-network

# Run mysql container but add it to my-network
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw  -e MYSQL_DATABASE=demo -v ~/Desktop/final_project:/var/lib/mysql --network my-network -dit mysql:latest --default-authentication-plugin=mysql_native_password

docker logs -f some-mysql


docker build -t link_api_image .
docker run  -dit --name=link_api -e FLASK_APP=webserver.py -p 5000:5000 --network my-network link_api_image

docker logs -f link_api