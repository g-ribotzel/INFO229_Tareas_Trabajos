docker-compose -f docker-compose.yml up -d --build db

echo "Por favor espere mientras la base de datos se esta inicializando."

sleep 120

echo "Listo!"

docker-compose -f docker-compose.yml up -d --build web