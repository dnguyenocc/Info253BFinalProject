# Creating a new network for my webserver container and my mysql database container
docker network create my-network

# Run mysql container but add it to my-network
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw  -e MYSQL_DATABASE=demo -v ~/Desktop/new_demo_db_folder:/var/lib/mysql --network my-network -dit mysql:latest --default-authentication-plugin=mysql_native_password


docker build -t documents_api_image .
docker run  -dit --name=documents_api -e FLASK_APP=webserver.py -p 5000:5000 --network my-network documents_api_image