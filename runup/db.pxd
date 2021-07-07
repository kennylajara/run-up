# cython: language_level=3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


cdef class RunupDB:

    cdef _dbname
    cdef bint _verbose
    cdef _conn

    cdef execute(self, name, query)

    cdef close_connection(self, bint commit)

    cdef connect(self)

    cdef insert_file(self, int job_id, char* path_from_pwd, path_from_yaml_file)

    cdef select_job(self, int job, project)
