docker stop chatbot-demo-chroma-server
docker rm chatbot-demo-chroma-server
docker stop chatbot-demo-memcached-server
docker rm chatbot-demo-memcached-server
cd ./db
docker-compose down
docker rmi chatbot-demo-main-db-image
cd ../
