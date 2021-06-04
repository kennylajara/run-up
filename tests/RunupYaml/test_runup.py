import unittest
from runup import RunupYAML

class TestRunupYAML(unittest.TestCase):

    def test__read_yaml_file(self):
        """Find a `runup.yml` in the given context."""
        
        # Search for runup.yaml
        RunupYAML()._read_yaml_file('./tests/RunupYaml/yaml')
        # Search for runup.yml
        RunupYAML()._read_yaml_file('./tests/RunupYaml/yml')
        # Shouldn't find the file
        with self.assertRaises(FileNotFoundError):
            RunupYAML()._read_yaml_file('./tests/RunupYaml/none')