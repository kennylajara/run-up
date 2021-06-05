# Built-in
from pathlib import Path
from typing import Union
import unittest

class TestCaseExtended(unittest.TestCase):

    def assertIsDir(self, path:Union[str, Path]):
        """Fail if the given pathis not a directory."""
        if not Path(path).resolve().is_dir():
            raise AssertionError("Directory does not exist: %s" % str(path))

    def assertIsFile(self, path:Union[str, Path]):
        """Fail if the given pathis not a file."""
        if not Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))