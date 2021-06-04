from setuptools import setup
from utils.runup import get_version

# Define setup
setup(
    name="RunUp",
    version=get_version(),
    py_modules=["runup"],
    install_requires=[
        'Click==8.0.1',
        'pyyaml==5.4.1',
    ],
    entry_points={
        'console_scripts': [
            'runup = main:cli',
        ],
    },
)