echo 'Build Dev Image'
docker build --pull --target=dev-base --network=host -t docker_name:dev-base .

echo 'Linter'
docker build --pull --target=dev-linter --network=host -t docker_name:dev-linter .

echo 'Utest Coverage'
docker build --pull --target=dev-coverage --network=host -t docker_name:dev-coverage .
docker create --name=container_name docker_name:dev-coverage
docker cp container_name:/var/test-output/. .
docker rm -v container_name

echo 'Build Prod Image'
docker build --network=host -t prod_docker .