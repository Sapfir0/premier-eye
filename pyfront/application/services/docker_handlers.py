
def runDockerContainer(name):
    import docker

    client = docker.from_env()
    # запуск контейнера
    client.containers.run(name, "python3 mainImage.py")
