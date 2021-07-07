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


cdef class RunupDB:
    """
    Handle the database where the data is stored.

    The `.runup` files are SQLite3 databases containing the
    path to the file, MD5 sign, SHA256 sign and ID of the backup
    where this file was found the first time.
    """

    def __init__(self, context: Path, bint verbose):

        self._dbname: str = str(f"{context}/.runup/runup.db")
        self._verbose: bint = verbose
        self._conn = None

    cdef execute(self, name, query):
        """Execute a query."""

        vInfo(self._verbose, f"Executed query: {name}")

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

    cdef close_connection(self, bint commit):
        """Close database connection"""

        vInfo(self._verbose, f"Closing connection to: {self._dbname}")
        if commit:
            self._conn.commit()
        self._conn.close()
        vInfo(self._verbose, b"Connetion closed")

    cdef connect(self):
        """Create a database connection to a `runup.db`."""
        vInfo(self._verbose, f"Creating connection to: {self._dbname}")

        try:
            self._conn = sqlite3.connect(self._dbname)
            vInfo(self._verbose, f"Database version: {sqlite3.version}")
        except Error as e:
            click.echo(e)

    def create_database(self):
        """Create a database `runup.db`."""

        sql_dict: Dict[bytes, bytes] = {
            "Create backups": """
            CREATE TABLE `backups` (
                `name` TEXT PRIMARY KEY,
                `running` INTEGER NOT NULL,
                `execute` INTEGER NULL
            );
        """,
            "Create jobs": """
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
        """,
            "Create files": """
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
        """,
            "Create signature index": """
            CREATE INDEX `idx_signature` ON `files` (`sha256`, `sha512`);
        """,
            "Create job_id index": """
            CREATE INDEX `idx_job_id` ON `files` (`job_id`);
        """,
        }

        self.connect()
        for name, sql in sql_dict.items():
            self.execute(name, sql)
        self.close_connection(commit=True)

    def insert_backup(self, name: str) -> None:
        """Insert a backup"""

        sql:str = f"""
            INSERT OR IGNORE
            INTO backups (name, running, execute)
            VALUES ('{name}', 0, NULL)
        """

        self.connect()
        self.execute("Insert backup", sql)
        self.close_connection(commit=True)

    cdef insert_file(
        self, int job_id, char* path_from_pwd, path_from_yaml_file
    ):
        """
        Insert a file into DB.

        Returns a boolean indicatinf if the inserted
        """
        sql:str

        sha256:str = hashfile(path_from_pwd, b"sha256")
        sha512:str = hashfile(path_from_pwd, b"sha512")

        self.connect()

        # TODO: Do not execute this query if is a directory (empty sha256 and sha512)
        sql = f"""
            SELECT file_id, sha256, sha512
            FROM files
            WHERE sha256='{sha256}' AND sha512='{sha512}'
            ORDER BY file_id ASC
            LIMIT 1;
        """

        result = self.execute(f"Search file: {path_from_yaml_file}", sql)
        

        inserted_new: bool

        if len(result) == 0:
            # Insert
            sql = f"""
                INSERT INTO files (job_id, sha256, sha512, path)
                VALUES ({job_id}, '{sha256}', '{sha512}', '{path_from_yaml_file}')
            """
            
            self.execute(f"Insert new file: {path_from_yaml_file}", sql)
            inserted_new = True
        else:
            # Insert
            sql = f"""
                INSERT INTO files (job_id, sha256, sha512, file_loc, path)
                VALUES ({job_id}, '{result[0][1]}', '{result[0][2]}', {result[0][0]}, '{path_from_yaml_file}')
            """

            self.execute(f"Insert existing file: {path_from_yaml_file}", sql)
            inserted_new = False

        self.close_connection(commit=True)

        return inserted_new

    def insert_job(self, backup_name: str):
        """Insert a job"""

        sql:str = f"""
            INSERT INTO jobs (job_id, backup_name, time_start, time_finish, files_num)
            VALUES (NULL, '{backup_name}', {int(time.time())}, NULL, 0)
        """

        self.connect()
        id: int = self.execute("Insert job", sql)
        self.close_connection(commit=True)

        return id

    cdef select_job(self, int job, project):
        """Select a job"""

        # Select latest job from DB
        if job == 0:

            sql:str = f"""
                SELECT MAX(files.job_id)
                FROM files
                JOIN jobs ON jobs.job_id = files.job_id
                WHERE jobs.backup_name = '{project}'
            """

            self.connect()
            job = self.execute("Select latest job", sql)[0][0]
            self.close_connection(commit=True)

        if job is None:
            return None

        # Select data from DB
        sql:str = f"""
            SELECT A.job_id, A.path, B.job_id, B.path
            FROM files AS A
            JOIN jobs ON jobs.job_id = A.job_id
            LEFT JOIN files AS B ON A.file_loc = B.file_id
            WHERE jobs.backup_name = '{project}' AND A.job_id = {job}
        """

        self.connect()
        data = self.execute("Get job info", sql)
        self.close_connection(commit=True)

        return data
