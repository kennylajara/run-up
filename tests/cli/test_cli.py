# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# Built-in    
import os
from pathlib import Path
from shutil import rmtree as rmdir_recursive
import sqlite3
from typing import List
import unittest
from unittest import mock
from zipfile import ZipFile

# 3rd party
from click.testing import CliRunner

# Own
from dev.unittest import TestCaseExtended
from runup.cli import cli
from runup.version import runup_version


class CLI_1_0(TestCaseExtended):
    """Test command line executions"""

    _context:str = './tests/cli/version-1.0'


    def setUp(self) -> None:
        
        # Init some tests
        runner:CliRunner = CliRunner()
        folders = [
            'create-backup-and-restore',
            'create-backup-implicit',
        ]
        for folder in folders:
            if not os.path.exists(f"{self._context}/{folder}/.runup"):
                runner.invoke(cli, ['--context', f'{self._context}/{folder}', 'init'])


    def tearDown(self) -> None:
        """Clean the environment after running the tests."""
        
        folders = [
            'create-backup-implicit',
            'create-backup-and-restore',
            'init',
        ]
        for folder in folders:
            if os.path.exists(f"{self._context}/{folder}/.runup"):
                rmdir_recursive(f"{self._context}/{folder}/.runup")

        restored_backup_dir = f"{self._context}/create-backup-and-restore/restore-here"
        for f in os.listdir(restored_backup_dir):
            if f == '.keep':
                continue

            path_to_delete:Path = Path(os.path.join(restored_backup_dir, f))
            if Path.is_dir(path_to_delete):
                rmdir_recursive(path_to_delete)
            else:
                os.remove(path_to_delete)


    def test_help(self):

        # Prepare
        runner:CliRunner = CliRunner()
        context:Path = f'{self._context}/init'
        # Execute
        result = runner.invoke(cli, ['--help', context])
        # Assert
        self.assertEqual(result.exit_code, 0)


    def test_init(self):

        # Prepare
        runner:CliRunner = CliRunner()
        context:Path = f'{self._context}/init'
        # Execute
        result = runner.invoke(cli, ['--context', context, 'init'])
        # Assert
        self.assertEqual(result.output, 'RunUp has been initialized successfully.\n')
        self.assertEqual(result.exit_code, 0)


    @mock.patch('runup.cli.click.echo', return_value=None)
    def test_init_verbose(self, mock_click_echo):

        # Prepare
        runner:CliRunner = CliRunner()
        context:Path = f'{self._context}/init-verbose'
        # Execute
        result = runner.invoke(cli, ['--verbose', '--context', context, 'init'])
        # Assert
        self.assertEqual(result.exit_code, 0)


    def test_version(self):

        # Prepare
        runner:CliRunner = CliRunner()
        # Execute
        result = runner.invoke(cli, ['--version'])
        # Assert
        self.assertEqual(result.output, f'RunUp, version {runup_version}\n')
        self.assertEqual(result.exit_code, 0)


    def test_create_backup_implicit(self):

        # Prepare
        runner:CliRunner = CliRunner()
        context:Path = f'{self._context}/create-backup-implicit'
        # Execute
        result = runner.invoke(cli, ['--context', context, 'backup'])  
        # Assert
        self.assertEqual(result.output, f'New backup created.\n')
        self.assertEqual(result.exit_code, 0)


    def test_create_backup_and_restore(self):

        # Prepare
        runner:CliRunner = CliRunner()
        context:Path = f'{self._context}/create-backup-and-restore'

        # ------------- #
        # Create Backup #
        # ------------- #
        result = runner.invoke(cli, ['--context', context, 'backup', 'myproject'])
        # Assert
        self.assertEqual(result.output, f'New backup created.\n')
        self.assertEqual(result.exit_code, 0)

        # Test job created
        self.assertIsFile(context + '/.runup/jobs/1')

        # Test files in job
        expected_zip_files_1:List[str] = [
            'dir-include/file.txt',
            'dir/file-1.txt', 
            'include.txt', 
        ]
        expected_zip_files_2:List[str] = [
            'dir-include/file.txt',
            'dir/file-2.txt', 
            'include.txt', 
        ]
        with ZipFile(context + '/.runup/jobs/1', 'r') as myzip:
            namelist:List[str] = myzip.namelist()
            namelist.sort()
            try:
                self.assertListEqual(namelist, expected_zip_files_1)
            except AssertionError:
                self.assertListEqual(namelist, expected_zip_files_2)

        # Test files in DB
        conn = sqlite3.connect(context + '/.runup/runup.db')
        cursor = conn.execute("SELECT path FROM 'files'")
        included_db_files:List[str] = []
        expected_db_files:List[str] = [
            './dir-include/file.txt',
            './dir/file-1.txt', 
            './dir/file-2.txt', 
            './include.txt', 
        ]
        for row in cursor:
            included_db_files.append(row[0])
        conn.close()
        included_db_files.sort()
        
        self.assertListEqual(expected_db_files, included_db_files)

        # -------------- #
        # Restore Backup #
        # -------------- #
        location:str = context + '/restore-here'
        result = runner.invoke(cli, ['--context', context, 'restore', '-f', '--location', location, 'myproject'])
        # Assert
        self.assertEqual(result.output, f'A backup for the project "myproject" has been restored.\n')
        self.assertEqual(result.exit_code, 0)

        # Test Files has been restored
        for file in expected_db_files:
            self.assertIsFile(location + os.sep + file)


if __name__ == "__main__":
    unittest.main()