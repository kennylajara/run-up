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
from runup import ParserYAML
from utils.runup import get_yaml_latest_version


class TestParserYAML(unittest.TestCase):

    @mock.patch('runup.click.echo', return_value=None)
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


    @mock.patch('runup.click.echo', return_value=None)
    def test__get_version(self, muck_click_echo):
        """Read the version of the a YAML file"""

        context:str = './tests/ParserYAML/version'
        expected_values:dict[str, Any] = {
            'missing-version': None,
            'unsupported-version': None,
            'version-non-string': None,
            'version-string': get_yaml_latest_version(),
        }

        for filename, expected_value in expected_values.items():
            with open(f'{context}/{filename}.yaml') as stream:
                yaml_content:dict = yaml.safe_load(stream)
                real_value = ParserYAML('.', True)._get_version(yaml_content)

            self.assertEqual(expected_value, real_value)
