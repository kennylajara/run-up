# RunUp

[![GitHub](https://img.shields.io/github/license/kennylajara/RunUp?style=for-the-badge&color=%230374b4)](https://github.com/kennylajara/RunUp/blob/main/LICENSE)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/RunUp?label=Python%20Support&style=for-the-badge)
[![PyPI](https://img.shields.io/pypi/v/RunUp?style=for-the-badge&color=%230374b4&label=Version&logoColor=%23ffffff)](https://pypi.org/project/RunUp/)


RunUp is a backup solution that implements a new backup strategy: Fragmented Backups. This solution solves all the drawback of the traditional backup strategies.

## Framented Backup

Traditionally, there are two ways of creating backups: Full backups and partial (incremental or differential) backups. Full backups duplicates data and are very slow to create, while partial backups reduce data duplication and are created faster but are slower to restore because you need to restore several partial backups.

We have devised the fragmented backups, a new backup strategy that creates partial backups but restores full backups, getting the best of both worlds.

### Save disk space

We don't duplicate unchanged files in your backup storage even if is duplicated in your repository or renamed at some point in the future.

### Create faster backups

RunUp only copy the new or changed files. This allow us to create the backups faster, saving you time and memory usage.

### Restore your backup faster

While restoring the data, we handle it as a full backup so we don't have the drawback of the tools implementing partial backup strategies.


## Usage

Install RunUp with PIP:

```
python3 -m pip install runup
```

Then you will need to config your backup and start using it. It is very easy, visit [Getting Started](https://runup.readthedocs/latest/getting-started) section of the documentation.

## Contribution

Contributions are welcome, either as an idea or as an implementations in the form of Pull Request. Do not hesitate to open a new issue to clarify doubts that may help the development of the product.

## License

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at [https://mozilla.org/MPL/2.0/](https://mozilla.org/MPL/2.0/).
