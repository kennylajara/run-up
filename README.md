# RunUp

[![GitHub](https://img.shields.io/github/license/kennylajara/RunUp?style=for-the-badge&color=%230374b4)](https://github.com/kennylajara/RunUp/blob/main/LICENSE)
[![Python version](https://img.shields.io/pypi/pyversions/RunUp?label=Python%20Support&style=for-the-badge)](https://runup.readthedocs.io/en/latest/getting-started/#requirements)
[![PyPI](https://img.shields.io/pypi/v/RunUp?style=for-the-badge&color=%230374b4&label=Version&logoColor=%23ffffff)](https://pypi.org/project/RunUp/)


RunUp is a backup solution that implements a new backup strategy: fragmented backups. This solution solves all the drawbacks of traditional strategies.

## Fragmented backup

There are three typical backup strategies: Full backups, incremental backups and differential backups:

* Full backups duplicate unmodified data and are very slow to create, but are easier and faster to restore. 

* Differential backups still create full backups (say weekly) and create partial backups _containing only the new and modified files since the last full backup_ (say daily). This may reduce data duplication somewhat and makes partial backups faster than the full backup, but it makes restore slower because you need to restore the last full backup and the last differential backup.

* Incremental backups work in the same way as differential backups but partial backups _only contain the files changed since the last full or partial backup_. This reduces data duplication even further and makes partial backups faster, but makes data restoration even slower, as you will have to restore the last full backup and all partial backups created after the full backup, in order.

With the above information in mind, I have come up with fragmented backups, a new backup strategy that only creates a full backup the first time, then all backups will be incremental backups. But the unchanged files are associated with the previously stored files, so during the backup restore, it is possible to "merge the fragments" and make the restore as fast as if it were a full backup.

## Key features

**Saves disk space**

Files are never duplicated in the backup storage, even if they are duplicated in the repository or renamed without changing the content.

**Create faster backups**

Each backup contains only one copy of new or changed files. This allows us to create backups faster, saving time and memory usage.

**Quick restoration of backups**

When restoring data, we handle it as a full backup, so we don't have the inconvenience of tools that implement traditional partial backup strategies.


## Usage

The installation with PIP will not work as I am still in the process to open source this project. To install it, follow the steps below:

```
# Clone the repo
git clone https://github.com/kennylajara/RunUp.git
# Get into the folder
cd RunUp
# Create and activate environment
python -m venv venv && source venv/bin/activate
# Install development dependencies
pip install -r requirements-dev.txt
# Compile (we are using Cython)
python setup.py build_ext --inplace
# Install package
pip install --editable .
# Test it has been installed successfully
runup --version 
# See how to use the package
runup --help
```

<!--
Install RunUp with PIP:

```
python3 -m pip install runup
```
-->

Create a `runup.yaml` file with the configuration of your backups. This is an example to back up all files in the same directory as the configuration file:

```
version: '1'

project:
  projectname:
    include: 
      - '.'
```

Initialize RunUp.

```
runup init
```

Create a backup

```
runup backup
```

Restore the latest backup

```
runup restore
```

For details or more advanced options, see the [documentation](https://runup.readthedocs.io/en/latest/).

## License

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at [https://mozilla.org/MPL/2.0/](https://mozilla.org/MPL/2.0/).

## Contribution

Contributions are welcome! See the [Contributor's Guide](https://github.com/kennylajara/RunUp/blob/main/CONTRIBUTING.md).

## Donation

This is a Free Open Source Software. If this project is of value to you, consider making a donation.

[![Donate me](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate?business=P8CT5NJ22N3UC&no_recurring=0&currency_code=USD)
