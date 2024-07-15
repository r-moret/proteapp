import uvicorn
from typing import Literal
import docker


def start(mode: Literal["dev", "prd"] = "dev"):
    if mode == "dev":
        docker_client = docker.from_env()
        container = docker_client.containers.run(
            "mongo", ports={"27017": 27017}, auto_remove=True, detach=True
        )

        uvicorn.run("proteapp.api.main:app", host="0.0.0.0", port=8000, reload=mode == "dev")
        container.remove(force=True)

    else:
        uvicorn.run("proteapp.api.main:app", host="0.0.0.0", port=8000)
