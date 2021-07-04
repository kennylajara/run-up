# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Buil-in
import os
from setuptools import Extension  # type: ignore


def get_modules(ext: str):

    ext_modules = []
    for root, _, files in os.walk("runup"):
        for file in files:
            if file.endswith(f".{ext}"):
                ext_modules += [
                    Extension(
                        f'{root.replace(os.sep, ".")}.{file[:-1*(len(ext)+1)]}',
                        [f"runup{os.sep}{file}"],
                    ),
                ]
    return ext_modules
