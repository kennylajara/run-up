# cython: language_level=3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# Built-in
from pathlib import Path
import sqlite3
from sqlite3 import Error
import time
from typing import Dict

# 3rd Party
import click
import pyximport  # type: ignore

pyximport.install()

# 3rd party - C
from libc.stdlib cimport malloc

# Own
from runup.utils cimport vInfo, hashfile


cdef struct sql_dict_type:
    char* sql_name
    char* sql_query


cdef class RunupDB:
    """
    Handle the database where the data is stored.

    The `.runup` files are SQLite3 databases containing the
    path to the file, MD5 sign, SHA256 sign and ID of the backup
    where this file was found the first time.
    """

    def __init__(self, context: Path, bint verbose):

        self._dbname = str(context) + "/.runup/runup.db"
        self._verbose = verbose
        self._conn = None

    cdef execute(self, str name, str query):
        """Execute a query."""

        vInfo(self._verbose, "Executed query: " + name)

        try:
            assert self._conn is not None
            c = self._conn.cursor()
            c.execute(query)
            if query.lower().strip().startswith("insert into "):
                return c.lastrowid
            elif query.lower().strip().startswith("insert or ignore into "):
                return c.lastrowid
            elif query.lower().strip().startswith("select "):
                return c.fetchall()
            return c
        except Error as e:
            click.echo(e)
            
    cdef void close_connection(self, bint commit):
        """Close database connection"""

        vInfo(self._verbose, "Closing connection to: " + self._dbname)
        if commit:
            self._conn.commit()
        self._conn.close()
        vInfo(self._verbose, "Connetion closed")

    cdef void connect(self):
        """Create a database connection to a `runup.db`."""
        vInfo(self._verbose, "Creating connection to: " + self._dbname)

        try:
            self._conn = sqlite3.connect(self._dbname)
            vInfo(self._verbose, "Database version: " + sqlite3.version)
        except Error as e:
            click.echo(e)

    cdef void create_database(self):
        """Create a database `runup.db`."""

        
        self.connect()
        self.execute("Create backups", """
            CREATE TABLE `backups` (
                `name` TEXT PRIMARY KEY,
                `running` INTEGER NOT NULL,
                `execute` INTEGER NULL
            );
        """)
        self.execute("Create jobs", """
            CREATE TABLE `jobs` (
                `job_id` INTEGER PRIMARY KEY,
                `backup_name` TEXT NOT NULL,
                `time_start` INTEGER NOT NULL,
                `time_finish` INTEGER NULL,
                `files_num` INTEGER NOT NULL,
                FOREIGN KEY (`backup_name`)
                REFERENCES `backups` (`backup_name`)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
        """)
        self.execute("Create files", """
            CREATE TABLE `files` (
                `file_id` INTEGER PRIMARY KEY,
                `job_id` INTEGER NOT NULL,
                `path` TEXT NOT NULL,
                `sha256` TEXT NOT NULL,
                `sha512` TEXT NOT NULL,
                `file_loc` INTEGER NULL,
                FOREIGN KEY (`job_id`)
                    REFERENCES `jobs` (`job_id`)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE,
                FOREIGN KEY (`file_loc`)
                    REFERENCES `jobs` (`file_loc`)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
            );
        """)
        self.execute("Create signature index", """
            CREATE INDEX `idx_signature` ON `files` (`sha256`, `sha512`);
        """)
        self.execute("Create job_id index", """
        CREATE INDEX `idx_job_id` ON `files` (`job_id`);
        """)

        self.close_connection(commit=True)

    cdef void insert_backup(self, str name):
        """Insert a backup"""

        self.connect()
        self.execute("Insert backup", 
            "INSERT OR IGNORE " + \
            "INTO backups (name, running, execute) " + \
            "VALUES ('"+ name +"', 0, NULL)"
        )
        self.close_connection(commit=True)

    cdef bint insert_file(self, int job_id, str path_from_pwd, str path_from_yaml_file):
        """
        Insert a file into DB.

        Returns a boolean indicatinf if the inserted
        """

        cdef str sha256
        cdef str sha512
        cdef bint inserted_new

        sha256 = hashfile(path_from_pwd, b"sha256")
        sha512 = hashfile(path_from_pwd, b"sha512")

        self.connect()

        # TODO: Do not execute this query if is a directory (empty sha256 and sha512)
        result = self.execute("Search file: " + path_from_yaml_file, 
            "SELECT file_id, sha256, sha512 " + \
            "FROM files " + \
            "WHERE sha256='"+sha256+"' AND sha512='"+sha512+"' " + \
            "ORDER BY file_id ASC " + \
            "LIMIT 1;"
        )

        if len(result) == 0:
            # Insert
            self.execute("Insert new file: "+path_from_yaml_file, 
                "INSERT INTO files (job_id, sha256, sha512, path) " + \
                "VALUES ("+str(job_id)+", '"+sha256+"', '"+sha512+"', '"+path_from_yaml_file+"')"
            )
            inserted_new = True
        else:
            # Insert
            self.execute("Insert existing file: "+path_from_yaml_file,
                "INSERT INTO files (job_id, sha256, sha512, file_loc, path) " + \
                "VALUES ("+str(job_id)+", '"+result[0][1]+"', '"+result[0][2]+"', "+str(result[0][0])+", '"+path_from_yaml_file+"')"
            )
            inserted_new = False

        self.close_connection(commit=True)

        return inserted_new

    cdef int insert_job(self, str backup_name):
        """Insert a job"""

        cdef int id 
        cdef str this_time 
        
        this_time = str(int(time.time()))
        
        self.connect()
        id = self.execute("Insert job", 
            "INSERT INTO jobs (job_id, backup_name, time_start, time_finish, files_num)" + \
            "VALUES (NULL, '" + backup_name + "', " + this_time + ", NULL, 0)"
        )
        self.close_connection(commit=True)

        return id

    cdef select_job(self, int job, str project):
        """Select a job"""

        cdef str sql

        self.connect()
        # Select latest job from DB
        if job == 0:
            job = self.execute("Select latest job",
                "SELECT MAX(files.job_id) " + \
                "FROM files " + \
                "JOIN jobs ON jobs.job_id = files.job_id " + \
                "WHERE jobs.backup_name = '"+project +"'"
            )[0][0]

        if job is None:
            return None

        # Select data from DB
        data = self.execute("Get job info", 
            "SELECT A.job_id, A.path, B.job_id, B.path " + \
            "FROM files AS A JOIN jobs ON jobs.job_id = A.job_id " + \
            "LEFT JOIN files AS B ON A.file_loc = B.file_id " + \
            "WHERE jobs.backup_name = '"+project+"' AND A.job_id = "+str(job)
        )
        self.close_connection(commit=True)

        return data
