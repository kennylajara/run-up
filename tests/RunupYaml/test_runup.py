from typing import Dict
import unittest

import yaml

from runup import RunupYAML


class TestRunupYAML(unittest.TestCase):

    def test__read_yaml_file(self):
        """Find a `runup.yml` in the given context."""
        
        # Search for runup.yaml
        yaml_file = RunupYAML()._read_yaml_file('./tests/RunupYaml/yaml')
        self.assertIsInstance(yaml_file, Dict)

        # Search for runup.yml
        yml_file = RunupYAML()._read_yaml_file('./tests/RunupYaml/yml')
        self.assertIsInstance(yml_file, Dict)

        # Shouldn't find the file
        no_file = RunupYAML()._read_yaml_file('./tests/RunupYaml/none')
        self.assertIsNone(no_file)

        # Shouldn't find the file
        no_file = RunupYAML()._read_yaml_file('./tests/RunupYaml/corrupted', debug=False)
        self.assertIsNone(no_file)

        # Shouldn't find the file
        no_file =    RunupYAML()._read_yaml_file('./tests/RunupYaml/corrupted', debug=True)
        self.assertIsNone(no_file)