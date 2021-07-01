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

### Saves disk space

Files are never duplicated in the backup storage, even if they are duplicated in the repository or renamed without changing the content.

### Create faster backups

Each backup contains only one copy of new or changed files. This allows us to create backups faster, saving time and memory usage.

### Quick restoration of backups

When restoring data, we handle it as a full backup, so we don't have the inconvenience of tools that implement traditional partial backup strategies.


## Usage

Install RunUp with PIP:

```
python3 -m pip install runup
```

Then you will have to [setup](https://runup.readthedocs.io/en/latest/setup/) the way the backups will be created before you are ready to start using it. Once you are ready, you can create backups with the following command:

```
runup backup
```

For a quick tutorial, visit the [Getting Started](https://runup.readthedocs.io/en/latest/getting-started/) section of the documentation.

## Contribution

Contributions are welcome, either as an idea or as an implementation in the form of a Pull Request. Do not hesitate to open a new issue to clarify doubts that may help the development of the product.

Donations are another way to contribute. If this project is of value to you, consider making a donation.

[![Donate me](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate?business=P8CT5NJ22N3UC&no_recurring=0&currency_code=USD)

## License

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at [https://mozilla.org/MPL/2.0/](https://mozilla.org/MPL/2.0/).
