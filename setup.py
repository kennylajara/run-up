from setuptools import setup
from src.utils.version import get_version

# Define setup
setup(
    name="RunUp",
    version=get_version(),
    #py_modules=["runup"],
    install_requires=[
        'Click==8.0.1',
        'pyyaml==5.4.1',
    ],
    entry_points={
        'console_scripts': [
            'runup = src.cli:cli',
        ],
    },
)