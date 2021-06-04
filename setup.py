from setuptools import setup

# Get version from `.version` file
with open('.version') as f:
    version = f.read()

# Define setup
setup(
    name="RunUp",
    version=version,
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