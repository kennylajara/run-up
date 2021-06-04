from setuptools import setup

with open('.version') as f:
    version = f.read()

setup(
    name="RunUp",
    version=version,
    py_modules=["runup", "main"],
    install_requires=[
        'Click==8.0.1',
    ],
    entry_points={
        'console_scripts': [
            'runup = main:cli',
        ],
    },
)