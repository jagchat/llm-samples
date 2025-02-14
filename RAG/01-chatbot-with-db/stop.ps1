cd ./docker-scripts
cd ./db
docker-compose down
docker rmi chatbot-demo-main-db-image #optional
cd ../memcached
docker-compose down
cd ../chroma
docker-compose down
cd ../../
