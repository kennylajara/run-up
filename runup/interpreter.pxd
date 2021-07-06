# cython: language_level=3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


cdef class Interpreter:

    cdef _context
    cdef _required_parameters
    cdef _valid_parameters
    cdef bint _verbose
    cdef _version

    cpdef bint create_backup(self, yaml_config, project)
    

cdef class Interpreter_1(Interpreter):

    cpdef bint create_backup(self, yaml_config, project)