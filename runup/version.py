# cython: language_level=3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# Built-in
from typing import List

# ----------------------------------------------- #
# Current version of runup                        #
# ----------------------------------------------- #
RUNUP_VERSION: str = "0.1b3"

# ----------------------------------------------------- #
# List of versions supported when reading the YAML file #
# ----------------------------------------------------- #
# Format: 2 numbers. Example: 1 and 1.0 but not 1.0.0   #
#                                                       #
# On every major release add a version X and a X.0      #
#                                                       #
# Until the release 2.0, a test is going to fail every  #
# time a new version is released. Just search for:      #
# "Update major to latest until 2.0 is released"        #
# without quotes.                                       #
# ----------------------------------------------------- #
YAML_VERSIONS: List[str] = [
    "1",
    "1.0",
]
