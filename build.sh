
docker build -t sapfir0/premier-eye:cpu -f pyback/docker/cpu/Dockerfile ./pyback
docker build -t sapfir0/premier-eye:web -f pyfront/Dockerfile ./pyfront
