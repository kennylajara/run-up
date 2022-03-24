#!/usr/bin/env python3

# Built-in
import os
from typing import Tuple
from sys import version_info as python_version
from setuptools import Extension, setup  # type: ignore


# 3rd party
import pyximport  # type: ignore

pyximport.install()



# ----------------------------------------------- #
# Current version of runup                        #
# ----------------------------------------------- #
RUNUP_VERSION: str = "0.1b4.1"

# ----------------------------------------------------- #
# List of versions supported when reading the YAML file #
# ----------------------------------------------------- #
# Format: 2 numbers. Example: 1 and 1.0 but not 1.0.0   #
#                                                       #
# On every major release add a version X and a X.0      #
#                                                       #
# Until the release 2.0, a test is going to fail every  #
# time a new version is released. Just search for:      #
# "Update major to latest until 2.0 is released"        #
# without quotes.                                       #
# ----------------------------------------------------- #
YAML_VERSIONS: Tuple[str] = (
    "1",
    "1.0",
)


def get_modules(exts):

    ext_modules = []
    for root, _, files in os.walk("runup"):
        for file in files:
            for ext in exts:
                if file.endswith(f".{ext}"):
                    ext_modules += [
                        Extension(
                            f'{root.replace(os.sep, ".")}.{file[:-1*(len(ext)+1)]}',
                            [f"runup{os.sep}{file}"],
                        ),
                    ]
    return ext_modules


# Validate Python version
if python_version[0] != 3 and python_version[1] not in [7, 8, 9]:
    raise Exception("Python version not supported")


# Set this to True to enable building extensions using Cython.
# Set it to False to build extensions from the C file (that
# was previously created using Cython).
# Set it to 'auto' to build with Cython if available, otherwise
# from the C file.
USE_CYTHON = True


if USE_CYTHON:
    try:
        from Cython.Distutils import build_ext  # type: ignore
    except ImportError:
        if USE_CYTHON == "auto":
            USE_CYTHON = False
        else:
            raise


if USE_CYTHON:
    ext_modules = get_modules(exts=['py', 'pyx'])
    cmdclass = {"build_ext": build_ext}
else:
    ext_modules = get_modules(exts=['c'])


# Get content of `README.md` to
# add it on the long description
with open("README.md", "r", encoding="utf-8") as f:
    README: str = f.read()


# Define setup
setup(
    name="RunUp",
    author="Kenny Lajara",
    author_email="kennylajara@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Mozilla Public License 1.0 (MPL)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: System :: Archiving :: Compression",
        "Topic :: System :: Recovery Tools",
    ],
    cmdclass=cmdclass,
    description="RunUp is a backup system that can be managed by command line.",
    entry_points={
        "console_scripts": [
            "runup = runup.cli:cli",
        ],
    },
    ext_modules=ext_modules,
    include_package_data=False,
    install_requires=[
        "Click==8.0.1",
        # "pillow==8.3.1",
        "pyyaml==6.0",
        "pygments==2.11.2",
    ],
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["runup"],
    package_dir={
        "runup": "runup",
    },
    project_urls={
        "Documentation": "https://runup.readthedocs.io/",
        "Tracker": "https://github.com/kennylajara/runup/issues",
        "Source": "https://github.com/kennylajara/runup",
    },
    python_requires=">=3.6",
    # url='https://github.com/kennylajara/runup',
    version=RUNUP_VERSION,
    zip_safe=False, # Prevent create a zipped egg file which will not work with cimport for pxd files
)
