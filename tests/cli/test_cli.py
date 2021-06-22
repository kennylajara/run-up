# Built-in    
import os
from pathlib import Path
from shutil import rmtree as rmdir_recursive
from unittest import mock

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
            'create-backup-explicit',
            'create-backup-implicit',
        ]
        for folder in folders:
            if not os.path.exists(f"{self._context}/{folder}/.runup"):
                runner.invoke(cli, ['--context', f'{self._context}/{folder}', 'init'])


    def tearDown(self) -> None:
        """Clean the environment after running the tests."""
        
        folders = [
            'create-backup-explicit',
            'create-backup-implicit',
            'init',
        ]
        for folder in folders:
            if os.path.exists(f"{self._context}/{folder}/.runup"):
                rmdir_recursive(f"{self._context}/{folder}/.runup")


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


    def test_create_backup_explicit(self):

        # Prepare
        runner:CliRunner = CliRunner()
        context:Path = f'{self._context}/create-backup-explicit'
        # Execute
        result = runner.invoke(cli, ['--context', context, 'backup', 'myproject'])  
        # Assert
        self.assertEqual(result.output, f'New backup created.\n')
        self.assertEqual(result.exit_code, 0)
