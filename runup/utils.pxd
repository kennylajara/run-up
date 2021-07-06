# cython: language_level=3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# Built-in
from typing import Any, Optional


cdef vInfo(verbose: bool, msg: str)

cdef vCall(verbose: bool, func: str)

cdef vResponse(verbose: bool, func: str, res: Optional[Any])

cpdef hash_bytestr_iter(bytesiter, hasher)

cpdef hashfile(fname, algo: str)