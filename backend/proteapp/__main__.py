import uvicorn
from typing import Literal
import docker
from docker.errors import DockerException


def start(mode: Literal["dev", "prd"] = "dev"):
    if mode == "dev":
        try:
            docker_client = docker.from_env()
            container = docker_client.containers.run(
                "mongo", ports={"27017": 27017}, auto_remove=True, detach=True
            )
        except DockerException:
            print(
                "Something happening while connecting to Docker. Do you have the Docker daemon initialized?"
            )
            return

        uvicorn.run("proteapp.api.main:app", host="0.0.0.0", port=8000, reload=mode == "dev")
        container.remove(force=True)

    else:
        uvicorn.run("proteapp.api.main:app", host="0.0.0.0", port=8000)
