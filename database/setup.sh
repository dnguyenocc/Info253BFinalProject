# Creating a new network for my webserver container and my mysql database container
docker network create my-network

# kill the old some-mysql
docker kill some-mysql
docker rm some-mysql

# Remove the old folder
rm -r ~/Desktop/new_demo_db_folder

# Run mysql container but add it to my-network
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw  -e MYSQL_DATABASE=demo -v ~/Desktop/new_demo_db_folder:/var/lib/mysql --network my-network -dit mysql:latest --default-authentication-plugin=mysql_native_password

# Let's make sure the mysql container is finished loading
docker logs -f some-mysql


