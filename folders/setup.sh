# Creating a new network for my webserver container and my mysql database container
docker network create my-network

# # Run mysql container but add it to my-network
# docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw  -e MYSQL_DATABASE=demo -v ~/Desktop/new_demo_db_folder:/var/lib/mysql --network my-network -dit mysql:latest --default-authentication-plugin=mysql_native_password

# kill and remove the old container
docker kill folders_api
docker rm folders_api


docker build -t folders_api_image .
docker run  -dit --name=folders_api -e FLASK_APP=webserver.py -p 5001:5001 --network my-network folders_api_image