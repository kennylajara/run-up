# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# Built-in
from typing import Dict, Optional
import unittest
from unittest import mock

# 3rd party
import pyximport  # type: ignore
import yaml

pyximport.install()

# Own
from runup.yaml_parser import ParserYAML


class TestParserYAML(unittest.TestCase):
    @mock.patch("runup.yaml_parser.click.echo", return_value=None)
    @mock.patch("runup.utils.echo", return_value=None)
    def test__read_yaml_file(self, muck_click_echo, muck_verbose):
        """Find a `runup.yml` in the given context."""

        # Type hint
        result: bool

        # directory: expected_result
        dir_tests: Dict[str, bool] = {
            "empty": False,
            "corrupted": False,
            "none": False,
            "yaml": True,
            "yml": True,
        }
        # Loop tests
        for directory, expected_success in dir_tests.items():

            result = ParserYAML(
                context='.', verbose=True  # Can be anything in this test
            )._read_yaml_file(f"./tests/ParserYAML/read/{directory}")

            # Assertions
            if expected_success is True:
                self.assertIsInstance(result, Dict)
            else:
                self.assertIsNone(result)

    @mock.patch("runup.yaml_parser.click.echo", return_value=None)
    @mock.patch("runup.utils.echo", return_value=None)
    def test__get_version(self, muck_click_echo, muck_verbose):
        """Read the version of the a YAML file"""

        context: str = "./tests/ParserYAML/version"

        # Do not remove or edit this comment
        # without reading the version.py :
        # "Update major to latest until 2.0 is released"
        expected_values: Dict[str, Optional[str]] = {
            "missing-version": None,
            "unsupported-version": None,
            "version-non-string": None,
            "version-string-minor": "1.0",
            "version-string-wrong": None,
            "version-string-major": "1.0",
        }

        for filename, expected_value in expected_values.items():
            with open(f"{context}/{filename}.yaml") as stream:
                yaml_content: Dict = yaml.safe_load(stream)
                real_value = ParserYAML('.', True)._get_version(yaml_content)

            self.assertEqual(expected_value, real_value)
