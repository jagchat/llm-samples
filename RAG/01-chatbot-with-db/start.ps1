cd ./db
docker compose up -d
cd ../
docker run -d -p 38000:8000 --name chatbot-demo-chroma-server  chromadb/chroma:0.6.3
docker run -d -p 31211:11211 --name chatbot-demo-memcached-server memcached:1.6.36

