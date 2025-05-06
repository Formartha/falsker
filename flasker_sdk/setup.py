from setuptools import setup, find_packages


with open("flasker_sdk/requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="flasker_sdk",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements,
)