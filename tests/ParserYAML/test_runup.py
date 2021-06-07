# Built-in
from pathlib import Path
from typing import (
    Any,
    Optional,
)
import unittest
from unittest import mock

# 3rd party
import yaml

# Own
from runup.yaml_parser import ParserYAML
from runup.version import yaml_versions


class TestParserYAML(unittest.TestCase):

    @mock.patch('runup.yaml_parser.click.echo', return_value=None)
    def test__read_yaml_file(self, muck_click_echo):
        """Find a `runup.yml` in the given context."""

        # Type hint
        path:Optional[Path]
        result:bool

        # directory: expected_result
        dir_tests:dict[str, bool] = {
            'yaml': True,
            'yml': True,
            'none': False,
            'corrupted': False,
        }
        # Loop tests
        for directory, expected_success in dir_tests.items():

            path, result = ParserYAML(
                context='.', # Can be anything in this test
                verbose=True
            )._read_yaml_file(f'./tests/ParserYAML/read/{directory}')

            # Assertions
            self.assertIsInstance(path, Path)
            if expected_success is True:
                self.assertIsInstance(result, dict)
            else:
                self.assertIsNone(result)


    @mock.patch('runup.yaml_parser.click.echo', return_value=None)
    def test__get_version(self, muck_click_echo):
        """Read the version of the a YAML file"""

        context:str = './tests/ParserYAML/version'

        # Do not remove or edit this comment  
        # without reading the version.py :
        # "Update major to latest until 2.0 is released"
        expected_values:dict[str, Any] = {
            'missing-version': None,
            'unsupported-version': None,
            'version-non-string': None,
            'version-string-minor': '1.0',
            'version-string-wrong': None,
            'version-string-major': '1.0',
        }

        for filename, expected_value in expected_values.items():
            with open(f'{context}/{filename}.yaml') as stream:
                yaml_content:dict = yaml.safe_load(stream)
                real_value = ParserYAML('.', True)._get_version(yaml_content)

            self.assertEqual(expected_value, real_value)
