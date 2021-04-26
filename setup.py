from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="reuther_digitization_utils",
    version="0.0.1",
    author="Walter P. Reuther Library",
    packages=find_packages(),
    description="Walter P. Reuther Library Digitization Utilities",
    install_requires=requirements
)
