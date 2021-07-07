# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# Built-in
from unittest import TestCase

# 3rd party
import pyximport  # type: ignore

pyximport.install()

# Own
from runup.utils import hashfile


class TestInterpreter_1(TestCase):
    def test_sha256(self):
        hash: str = hashfile(b"./tests/utils/hash/hello_world.txt", b"sha256")
        self.assertEqual(
            hash, "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
        )

    def test_sha512(self):
        hash: str = hashfile(b"./tests/utils/hash/hello_world.txt", b"sha512")
        expected: str = (
            "374d794a95cdcfd8b35993185fef9ba368f160d8daf432d08ba9f1ed1e5abe6cc"
            + "69291e0fa2fe0006a52570ef18c19def4e617c33ce52ef0a6e5fbe318cb0387"
        )
        self.assertEqual(hash, expected)

    def test_invalid_hash(self):
        with self.assertRaises(ValueError):
            hashfile(b"./tests/utils/hash/hello_world.txt", b"md1")
