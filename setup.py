import os
import re
import sys

from setuptools import find_packages, setup

with open("module_name.txt", "r") as file:
    module_name = file.read()
path_file_init_file = os.path.join(module_name, "__init__.py")

with open(path_file_init_file) as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)  # type: ignore
with open(path_file_init_file) as f:
    package_name = re.search(r'^__title__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)  # type: ignore

requirements = []
with open("requirements.txt") as file:
    requirements = file.read().splitlines()

if sys.platform.startswith("win32"):
    requirements.append("torch @ https://download.pytorch.org/whl/cpu/torch-1.7.1%2Bcpu-cp38-cp38-win_amd64.whl")
else:
    requirements.append("#torch @ https://download.pytorch.org/whl/cpu/torch-1.7.1%2Bcpu-cp38-cp38-linux_x86_64.whl")

with open("requirements_internal.txt") as file:
    requirements_internal = file.read().splitlines()

print(requirements)
requirements.extend(requirements_internal)
print(requirements)

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name=package_name,
    version=version,
    install_requires=requirements,
    packages=find_packages(),
    package_data={},
    python_requires=">=3.8",
    author="Jaap Oosterbroek",
    author_email="jaap@arrayinsights.com",
    description="Arin patient story app.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://nowhere.not",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: SAIL :: Propritary",
        "Operating System :: OS Independent",
    ],
)
