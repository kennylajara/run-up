# Built-in
from pathlib import Path
from typing import (
    Any,
    Dict,
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
        corrupted_file:None
        no_file:None
        path:Path
        yaml_file:Dict
        yml_file:Dict

        # Search for runup.yaml
        path, yaml_file = ParserYAML('.', True)._read_yaml_file('./tests/ParserYAML/read/yaml')
        self.assertIsInstance(path, Path)
        self.assertIsInstance(yaml_file, Dict)

        # Search for runup.yml
        path, yml_file = ParserYAML('.', True)._read_yaml_file('./tests/ParserYAML/read/yml')
        self.assertIsInstance(path, Path)
        self.assertIsInstance(yml_file, Dict)

        # Shouldn't find the file
        path, no_file = ParserYAML('.', True)._read_yaml_file('./tests/ParserYAML/read/none')
        self.assertIsInstance(path, Path)
        self.assertIsNone(no_file)

        # Shouldn't find the file
        path, corrupted_file = ParserYAML('.', True)._read_yaml_file('./tests/ParserYAML/read/corrupted')
        self.assertIsInstance(path, Path)
        self.assertIsNone(corrupted_file)

    @mock.patch('runup.click.echo', return_value=None)
    def test__get_version(self, muck_click_echo):
        """Read the version of the a YAML file"""

        context:str = './tests/ParserYAML/version'
        expected_values:Dict[str, Any] = {
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
