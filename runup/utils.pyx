# cython: language_level=3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# Built-in
import hashlib
from os.path import isdir

# 3rd party
from click import echo


# ------- #
# VERBOSE #
# ------- #


cdef void vInfo(bint verbose, msg):
    """Print verbose Info"""
    if verbose:
        echo(f"Info: {msg}")


cdef void vCall(bint verbose, func):
    """Print verbose Call"""
    if verbose:
        echo(f"Call: {func}")


cdef void vResponse(bint verbose, func, res):
    """Print verbose Response"""
    if verbose:
        echo(f"Response: {func} => {res}")


# -------------- #
# HASH FUNCTIONS #
# -------------- #


cpdef hash_bytestr_iter(bytesiter, hasher):
    for block in bytesiter:
        hasher.update(block)
    return hasher.hexdigest()


def file_as_blockiter(afile, blocksize: int=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)


cpdef hashfile(char* fname, char* algo):
    algorithm: hashlib._Hash

    if algo == b"sha256":
        algorithm = hashlib.sha256()
    elif algo == b"sha512":
        algorithm = hashlib.sha512()
    else:
        raise ValueError(f"Unsupported hash algorithm: {algo}")

    if isdir(fname):
        return ""

    return hash_bytestr_iter(file_as_blockiter(open(fname, "rb")), algorithm)
