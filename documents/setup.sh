# kill and remove the old container
docker kill link_api
docker rm link_api

# build a new container
docker build -t link_api_image .
docker run  -dit --name=link_api -e FLASK_APP=webserver.py -p 5000:5000 --network my-network link_api_image


docker logs -f link_api