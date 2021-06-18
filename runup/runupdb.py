# Built-in
from hashlib import sha256
from pathlib import Path
import sqlite3
from sqlite3 import Error
import time;
from typing import Dict

# 3rd Party
import click

# Own
from runup.utils import vCall, vInfo, vResponse, hashfile


class RunupDB:
    """
    Handle the database where the data is stored.
    
    The `.runup` files are SQLite3 databases containing the
    path to the file, MD5 sign, SHA256 sign and ID of the backup
    where this file was found the first time.
    """
    
    def __init__(self, context:Path, verbose:bool):

        self._dbname:Path = f'{context}/.runup/runup.db'
        self._verbose:bool = verbose
        self._conn = None


    def execute(self, name:str, query:str):
        """Execute a query."""

        vInfo(self._verbose, f'Executed query: {name}')

        try:
            c = self._conn.cursor()
            c.execute(query)
            if query.lower().strip().startswith('insert into '):
                return c.lastrowid
            elif query.lower().strip().startswith('insert or ignore into '):
                return c.lastrowid
            return c
        except Error as e:
            click.echo(e)


    def close_connection(self, commit=True):
        """Close database connection"""

        vInfo(self._verbose, f'Closing connection to: {self._dbname}')
        if commit:
            self._conn.commit()
        self._conn.close()
        vInfo(self._verbose, f'Connetion closed')


    def connect(self):
        """Create a database connection to a `runup.db`."""
        vInfo(self._verbose, f'Creating connection to: {self._dbname}')

        try:
            self._conn = sqlite3.connect(self._dbname)
            vInfo(self._verbose, f'Database version: {sqlite3.version}')
        except Error as e:
            click.echo(e)
        

    def create_database(self):
        """Create a database `runup.db`."""

        sql_dict:Dict[str] = {
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
                `job_loc` INTEGER NOT NULL,
                FOREIGN KEY (`job_id`)
                    REFERENCES `jobs` (`job_id`)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE,
                FOREIGN KEY (`job_loc`)
                    REFERENCES `jobs` (`job_loc`)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
            );
        """,
        "Create signature index": """
            CREATE UNIQUE INDEX `signature` 
            ON `files` (`sha256`, `sha512`);
        """,
        }

        self.connect()
        for name, sql in sql_dict.items():
            self.execute(name, sql)
        self.close_connection()


    def insert_backup(self, name:str) -> bool:
        """Insert a backup"""

        sql:str = f"""
            INSERT OR IGNORE
            INTO backups (name, running, execute)
            VALUES ('{name}', 0, NULL)
        """

        self.connect()
        self.execute('Insert backup', sql)
        self.close_connection()


    def insert_file(self, job_id:int, filename:str):
        """Insert a file"""

        sha256:str = hashfile(filename, "sha256")
        sha512:str = hashfile(filename, "sha512")

        self.connect()

        # Find
        if sha256 == 'dir' or sha512 == 'dir':
            sql:str = f"""
                SELECT sha256, sha512, job_loc
                FROM files
                WHERE sha256='{sha256}' AND sha512='{sha512}' AND path='{filename}'
                LIMIT 1;
            """
        else:
            sql:str = f"""
                SELECT sha256, sha512, job_loc
                FROM files
                WHERE sha256='{sha256}' AND sha512='{sha512}'
                LIMIT 1;
            """

        cursor = self.execute(f'Insert file: {filename}', sql)
        result = cursor.fetchall()
        id:int 

        if len(result) == 0:
            # Insert
            sql:str = f"""
                INSERT OR IGNORE INTO files (job_id, sha256, sha512, job_loc, path)
                VALUES ({job_id}, '{sha256}', '{sha512}', {job_id}, '{filename}')
            """
            id = self.execute(f'Insert file: {filename}', sql)
        else:
            # Insert
            sql:str = f"""
                INSERT OR IGNORE INTO files (job_id, sha256, sha512, job_loc, path)
                VALUES ({job_id}, '{result[0][0]}', '{result[0][1]}', {result[0][2]}, '{filename}')
            """
            id = self.execute(f'Insert file: {filename}', sql)

        self.close_connection()

        return id


    def insert_job(self, backup_name:str):
        """Insert a job"""

        sql:str = f"""
            INSERT INTO jobs (job_id, backup_name, time_start, time_finish, files_num)
            VALUES (NULL, '{backup_name}', {int(time.time())}, NULL, 0)
        """

        self.connect()
        id:str = self.execute('Insert job', sql)
        self.close_connection()

        return id
