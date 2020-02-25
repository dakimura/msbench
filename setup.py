from setuptools import setup

setup(
    name="msbench",
    version="1.0.1",
    description="Benchmarking tool for marketstore",
    author="Daito Akimura",
    install_requires=["pymarketstore", "argparse", ],
    entry_points={
        "console_scripts": [
            "msbench = app:main"
        ]
    }
)
