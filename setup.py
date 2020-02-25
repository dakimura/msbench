# -*- coding: utf-8 -*-

from io import open
from setuptools import setup, find_packages

with open('README.md', encoding="utf-8") as f:
    readme = f.read()

with open('LICENSE', encoding="utf-8") as f:
    license = f.read()

setup(
    name="msbench",
    version="1.0.6",
    description="Benchmarking tool for marketstore",
    author="Daito Akimura",
    install_requires=["pymarketstore", "argparse", ],
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        "console_scripts": [
            "msbench = msbench.app:main",
        ]
    }
)
