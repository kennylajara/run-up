# Built-in
import os
from pathlib import Path
from shutil import rmtree as rmdir_recursive
from typing import List
from unittest import mock

# Own
from dev.unittest import TestCaseExtended
from runup.interpreter import Interpreter_1
from runup.yaml_parser import ParserYAML


class TestInterpreter_1(TestCaseExtended):

    _context:str = './tests/Interpreter/Interpreter_1'
    _version:str = '1'

    def tearDown(self) -> None:
        """Clean the environment after running the tests."""
        if os.path.exists(f"{self._context}/set_environment/empty/.runup"):
            rmdir_recursive(f"{self._context}/set_environment/empty/.runup")

    @mock.patch('runup.interpreter.click.echo', return_value=None)
    @mock.patch('runup.utils.echo', return_value=None)
    def test_set_environment_success(self, muck_click_echo, muck_verbose) -> None:
        """Test: `Interpreter_1.set_environment`"""

        context:Path = f'{self._context}/set_environment/empty'
        env_is_set:bool = Interpreter_1(context, True).set_environment()
        self.assertTrue(env_is_set)

        # Confirm that the expected directory have been created
        dir_path:Path = Path(f'{context}/.runup')
        self.assertIsDir(dir_path)

        # Confirm that the expected files has been created
        expected_files = [
            '.version',
            'runup.db',
        ]
        for expected_file in expected_files:
            file_path:Path = Path(f'{context}/.runup/{expected_file}')
            self.assertIsFile(file_path)

        # Confirm that the `.version` file hast the right version
        with open(f'{context}/.runup/.version') as f:
            self.assertEqual(f.read(), self._version)


    @mock.patch('runup.interpreter.click.echo', return_value=None)
    @mock.patch('runup.utils.echo', return_value=None)
    def test_set_environment_fail(self, muck_click_echo, muck_verbose) -> None:
        """Test: `Interpreter_1.set_environment`"""
        
        directories:List[str] = [
            'dir-exists',
        ]

        for directory in directories:
            context:Path = f'{self._context}/set_environment/{directory}'
            env_is_set:bool = Interpreter_1(context, True).set_environment()
            self.assertFalse(env_is_set)