from setuptools import setup, find_packages

setup(
    name="featly",
    author="tian.luan",
    author_email="luan.tian@outlook.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)