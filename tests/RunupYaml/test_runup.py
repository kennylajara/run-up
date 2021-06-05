from typing import (
    Any,
    Dict,
    Optional,
)
import unittest

import yaml

from runup import RunupYAML
from utils.runup import get_yaml_latest_version


class TestRunupYAML(unittest.TestCase):

    def test__read_yaml_file(self):
        """Find a `runup.yml` in the given context."""
        
        # Search for runup.yaml
        yaml_file:Dict = RunupYAML('.')._read_yaml_file('./tests/RunupYaml/read/yaml')
        self.assertIsInstance(yaml_file, Dict)

        # Search for runup.yml
        yml_file:Dict = RunupYAML('.')._read_yaml_file('./tests/RunupYaml/read/yml')
        self.assertIsInstance(yml_file, Dict)

        # Shouldn't find the file
        no_file:None = RunupYAML('.')._read_yaml_file('./tests/RunupYaml/read/none')
        self.assertIsNone(no_file)

        # Shouldn't find the file
        corrupted_file:None = RunupYAML('.')._read_yaml_file('./tests/RunupYaml/read/corrupted')
        self.assertIsNone(corrupted_file)

    def test__get_version(self):
        """Read the version of the a YAML file"""

        context:str = './tests/RunupYaml/version'
        expected_values:Dict[str, Any] = {
            'missing-version': None,
            'unsupported-version': None,
            'version-non-string': None,
            'version-string': '1',
        }

        for filename, expected_value in expected_values.items():
            with open(f'{context}/{filename}.yaml') as stream:
                yaml_content:dict = yaml.safe_load(stream)
                real_value = RunupYAML('.')._get_version(yaml_content)

            self.assertEqual(expected_value, real_value)

