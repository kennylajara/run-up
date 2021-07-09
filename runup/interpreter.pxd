# cython: language_level=3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


cdef class Interpreter:

    cdef _context
    cdef _required_parameters
    cdef _valid_parameters
    cdef bint _verbose
    cdef char* _version

    cpdef bint create_backup(self, yaml_config, project)
    
    cpdef restore_backup(self, yaml_config: Dict[str, Any], str project, str location, int job, bint force)
    

cdef class Interpreter_1(Interpreter):

    cpdef bint create_backup(self, yaml_config, project)
    
    cpdef restore_backup(self, yaml_config: Dict[str, Any], str project, str location, int job, bint force)

    cdef _working_directories(self, config: Dict[str, Any])

    cdef _validate_prev_init(self, yaml_config: Dict[str, Any])