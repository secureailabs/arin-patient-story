import os
import re
import subprocess

from build_docker import build_docker
from start_docker import start_docker

if __name__ == "__main__":

    with open("app/__init__.py") as file:
        version_module = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)  # type: ignore
    with open("app/__init__.py") as file:
        title = re.search(r'^__title__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)  # type: ignore
    image_name = f"arin/{title}-image"
    image_tag = version_module
    conainer_name = f"{title}-container"
    print(image_tag)
    build_docker(image_name, image_tag)
    start_docker(image_name, image_tag, conainer_name)
