# cython: language_level=3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# 3rd party
import pyximport  # type: ignore

pyximport.install()

# Own
from runup.interpreter cimport Interpreter


cdef class ParserYAML:
    """Analizer of the `runup.yml` or `runup.yaml` file."""

    cdef _context
    cdef Interpreter _interpreter
    cdef bint _verbose

    cpdef parse(self)

    cpdef _read_yaml_file(self, context:str)