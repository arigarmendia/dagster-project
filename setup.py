from setuptools import find_packages, setup

setup(
    name="rec_sys",
    packages=find_packages(exclude=["rec_sys_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
