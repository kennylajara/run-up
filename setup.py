import setuptools 


# Get content of `.version` to 
# add it on the long description
with open('.version', "r", encoding="utf-8") as f:
    VERSION:str = f.read()

# Get content of `README.md` to 
# add it on the long description
with open('README.md', "r", encoding="utf-8") as f:
    README:str = f.read()


# Define setup
setuptools.setup(
    name="RunUp",
    author="Kenny Lajara",
    author_email="kennylajara@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        'Intended Audience :: Developers',
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Topic :: System :: Archiving :: Backup",
        "Topic :: System :: Archiving :: Compression",
        "Topic :: System :: Recovery Tools",
    ],
    description="RunUp is a backup system that can be managed by command line.",
    entry_points={
        'console_scripts': [
            'runup = src.runup.cli:cli',
        ],
    },
    include_package_data=True,
    install_requires=[
        'Click==8.0.1',
        'pyyaml==5.4.1',
    ],
    long_description=README,
    long_description_content_type="text/markdown",
    project_urls={
        # "Documentation": "https://readthedocs.org/",
        # 'Source': "https://github.com/kennylajara/runup",
        'Tracker': 'https://github.com/kennylajara/runup/issues',
    },
    python_requires='>=3.6',
    url="https://github.com/kennylajara/runup",
    version=VERSION,
)