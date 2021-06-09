# Built-in
from pathlib import Path
import sqlite3
from sqlite3 import Error
from typing import Dict

# 3rd Party
import click


class RunupDB:
    """
    Handle the database where the data is stored.
    
    The `.runup` files are SQLite3 databases containing the
    path to the file, MD5 sign, SHA256 sign and ID of the backup
    where this file was found the first time.
    """
    
    def __init__(self, context:Path, verbose:bool):
        self._dbname:Path = Path(f'{context}/.runup/runup.db')
        self._verbose:bool = verbose
        self._conn = None
        
    def execute(self, name:str, query:str):
        """Execute a query."""

        if self._verbose:
            click.echo(f'Executed query: {name}')

        try:
            c = self._conn.cursor()
            c.execute(query)
        except Error as e:
            click.echo(e)

    def close_connection(self):
        """Close database connection"""

        if self._verbose:
            click.echo(f'Closing connection to: {self._dbname}')
        self._conn.close()
        if self._verbose:
            click.echo(f'Connetion closed')

    def connect(self):
        """Create a database connection to a `runup.db`."""
        if self._verbose:
            click.echo(f'Creating connection to: {self._dbname}')

        try:
            self._conn = sqlite3.connect(self._dbname)
            if self._verbose:
                click.echo(f'Database version: {sqlite3.version}')
        except Error as e:
            click.echo(e)
        
    def create_database(self):
        """Create a database `runup.db`."""

        sql_dict:Dict[str] = {
        "Create procedures": """
            CREATE TABLE `procedures` (
                `name` TEXT PRIMARY KEY,
                `running` BOOL NOT NULL,
                `source` TEXT NOT NULL,
                `cron` TEXT NOT NULL
            );
        """,
        "Create jobs": """
            CREATE TABLE `jobs` (
                `job_id` INTEGER PRIMARY KEY,
                `procedure_name` TEXT NOT NULL,
                `time_start` DATETIME NOT NULL,
                `time_finish` DATETIME NULL,
                `files_num` INT NOT NULL,
                FOREIGN KEY (`procedure_name`)
                REFERENCES `procedures` (`procedure_name`)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
        """,
        "Create files": """
            CREATE TABLE `files` (
                `file_id` INTEGER PRIMARY KEY,
                `job_id` INTEGER NOT NULL,
                `path` TEXT NOT NULL,
                `md5` TEXT NOT NULL,
                `sha1` TEXT NOT NULL,
                `sha2` TEXT NOT NULL,
                FOREIGN KEY (`job_id`)
                REFERENCES `jobs` (`job_id`)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
        """,
        "Create signature index": """
            CREATE UNIQUE INDEX `signature` 
            ON `files` (`md5`, `sha1`, `sha2`);
        """,
        }

        self.connect()
        for name, sql in sql_dict.items():
            self.execute(name, sql)
        self.close_connection()
