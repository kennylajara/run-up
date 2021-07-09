# cython: language_level=3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# 3rd party
import pyximport  # type: ignore

pyximport.install()

# Own
from runup.interpreter cimport Interpreter


cdef class Config(object):
    """Default config of the "Global" args and kwargs."""
    
    cdef str context
    cdef bint verbose
    cdef Interpreter interpreter
    cdef yaml