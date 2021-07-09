# cython: language_level=3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


cdef class RunupDB:

    cdef str _dbname
    cdef bint _verbose
    cdef _conn

    cdef execute(self, str name, str query)

    cdef void close_connection(self, bint commit)

    cdef void connect(self)

    cdef void create_database(self)

    cdef void insert_backup(self, str name)

    cdef bint insert_file(self, int job_id, str path_from_pwd, str path_from_yaml_file)
    
    cdef int insert_job(self, str backup_name)

    cdef select_job(self, int job, str project)
