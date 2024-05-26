from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="netbits",
    version="0.0.1",
    author="Samuel Hulme",
    description="Convert data into structured packets and make packet handling a breeze!",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ajh123/netbits"
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)