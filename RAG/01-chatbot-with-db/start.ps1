cd ./docker-scripts
cd ./db
docker compose up -d
cd ../memcached
docker compose up -d
cd ../chroma
docker compose up -d
cd ../../

