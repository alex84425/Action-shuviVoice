echo 'Build Dev Image'
docker build --pull --target=dev-base --network=host -t docker_name:dev-base .

echo 'Linter'
docker build --pull --target=dev-linter --network=host -t docker_name:dev-linter .

echo 'Utest Coverage'
docker build --pull --target=dev-coverage --network=host -t docker_name:dev-coverage .
docker create --name=container_name docker_name:dev-coverage
docker cp container_name:/app/coverage.xml .
docker cp container_name:/app/htmlcov .
docker rm -v container_name

echo 'Security'
docker build --pull --target=dev-security --network=host -t docker_name:dev-security .

echo 'Build Prod Image'
docker build --network=host -t prod_docker .
