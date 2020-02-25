from setuptools import setup

setup(
    name="msbench",
    version="1.0",
    description="Benchmarking tool for marketstore",
    author="Daito Akimura",
    install_requires=["pymarketstore", "ArgumentParser", ],
    entry_points={
        "console_scripts": [
            "msbench = app:main"
        ]
    }
)
