# cython: language_level=3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# Built-in
from typing import Any, Optional
import hashlib
from os.path import isdir

# 3rd party
from click import echo


# ------- #
# VERBOSE #
# ------- #


def vInfo(verbose: bool, msg: str) -> None:
    """Print verbose Info"""
    if verbose:
        echo(f"Info: {msg}")


def vCall(verbose: bool, func: str) -> None:
    """Print verbose Call"""
    if verbose:
        echo(f"Call: {func}")


def vResponse(verbose: bool, func: str, res: Optional[Any]) -> None:
    """Print verbose Response"""
    if verbose:
        echo(f"Response: {func} => {res}")


# -------------- #
# HASH FUNCTIONS #
# -------------- #


def hash_bytestr_iter(bytesiter, hasher):
    for block in bytesiter:
        hasher.update(block)
    return hasher.hexdigest()


def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)


def hashfile(fname, algo: str):
    algorithm: hashlib._Hash

    if algo == "sha256":
        algorithm = hashlib.sha256()
    elif algo == "sha512":
        algorithm = hashlib.sha512()
    else:
        raise ValueError(f"Unsupported hash algorithm: {algo}")

    if isdir(fname):
        return ""

    return hash_bytestr_iter(file_as_blockiter(open(fname, "rb")), algorithm)
