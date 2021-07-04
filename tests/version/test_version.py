# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# Built-in
import re
from typing import List, Pattern
import unittest

# 3rd party
import pyximport  # type: ignore

pyximport.install()

# Own
from runup.version import runup_version, yaml_versions


class TestParserYAML(unittest.TestCase):
    def test_runup_version(self):
        """Confirm that the verion is well formated."""
        self.assertIsInstance(runup_version, str)
        self.assertNotEqual(runup_version, "")
        # semver = re.compile(r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)' + \
        # '(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?' + \
        # '(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$')

        # self.assertRegex(runup_version, semver)

    def test_yaml_versions(self):
        """Test valid versions of YAML files"""
        self.assertIsInstance(yaml_versions, List)
        for version in yaml_versions:
            self.assertIsInstance(version, str)
            format: Pattern[str] = re.compile(r"^(0|[1-9]\d*)(\.(0|[1-9]\d*))?$")
            self.assertRegex(version, format)
