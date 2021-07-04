#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# Built-in
from sys import version_info
from setuptools import setup  # type: ignore

# Own
from dev import build
from runup.version import RUNUP_VERSION


# Validate Python version
if version_info[0] != 3 and version_info[1] not in [7, 8, 9]:
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
    ext_modules = build.get_modules(ext="py")
    cmdclass = {"build_ext": build_ext}
else:
    ext_modules = build.get_modules(ext="c")


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
    include_package_data=True,
    install_requires=[
        "Click==8.0.1",
        "pyyaml==5.4.1",
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
)
