# kill the old some-mysql
docker kill folders_api
docker rm folders_api

## Remove the old folder
#rm -r ~/Desktop/new_demo_db_folder

## Run mysql container but add it to my-network
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw  -e MYSQL_DATABASE=demo -v ~/Desktop/new_demo_db_folder:/var/lib/mysql --network my-network -dit mysql:latest --default-authentication-plugin=mysql_native_password

docker build -t folders_api_image .
docker run  -dit --name=folders_api -e FLASK_APP=webserver.py -p 5001:5001 --network my-network folders_api_image

docker logs -f folders_api