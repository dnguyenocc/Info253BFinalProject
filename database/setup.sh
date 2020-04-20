# Creating a new network for my webserver container and my mysql database container
docker network create my-network

# Run mysql container but add it to my-network
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw  -e MYSQL_DATABASE=demo -v ~/Desktop/new_demo_db_folder:/var/lib/mysql --network my-network -dit mysql:latest --default-authentication-plugin=mysql_native_password

# Let's make sure the mysql container is finished loading
docker logs -f some-mysql

# Let's now tell docker to execute a command (bash) in the some-mysql container and make it interactive so that we can run commands inside the some-mysql container in another process (i.e. don't stop the mysql process within the docker container)
docker exec -it some-mysql bash

# Now we are inside the mysql container in a separate process. Let's run the mysql client app so that we can execute SQL queries
mysql -uroot -p

# Let's now display all of the databases inside the MySQL instance
show databases;

# Let's select the demo database we created on initialization
use demo;

# We are now in the database. We can now create tables and run query commands. To verify that we have no tables, let's view all of the tables;
show tables;