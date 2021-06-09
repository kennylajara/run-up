# RunUp

![GitHub](https://img.shields.io/github/license/kennylajara/RunUp?style=for-the-badge&color=%230374b4)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/RunUp?label=Python%20Support&style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/RunUp?style=for-the-badge&color=%230374b4&label=Version&logoColor=%23ffffff)


RunUp is a backup system that can be managed by command line. It is intended to be easy to use, secure and fast.

### Why yet another backup solution?

Most backup solutions are good at making full backups, but this can be time-consuming and unchanged data is replicated each time a new backup is made.

Some other solutions implement differential backups and incremental backups, two strategies that _partially_ solve this drawback. But that's the problem with them.... "partially". With incremental backups and differential backups restoring the data takes a long time, and.... So how do they solve it? By creating full backups from time to time. [_Facepalm_]

An then there are Git based solutions. Well, Git is excellent for code versioning but when you talk about backups... let's says that this is not what it was designed for. The Git history cannot be changed, to do simple tasks such as deleting the oldest restore points or moving to some files to cool storage, one would have to resort to dubious strategies. I don't know how they implement it (or if the they do it), but I'm not sure if I want to know...

And then the well-known big file issue. Let's quote what the creator of Git said about that:

> And yes, then there’s the “big file” issues. I really don’t know what to do about huge files. We suck at them, I know.
> 
> — Linus Torvalds ([source](https://towardsdatascience.com/data-versioning-all-you-need-to-know-7077aa5ed6d1#d5e7))

So, why yet another backup solution? Because we need to finally solves these issues and this is what this tool does by creating "fractional backups". A new backup strategy that not only reduces restore time, but completely avoids data duplication.

## Usage

Unfortunately it is not ready yet, so it cannot be used. I am working hard on it.

## Contribution

Contributions are welcome, either as an idea or as an implementations in the form of Pull Request. Do not hesitate to open a new issue to clarify doubts that may help the development of the product.

## License

This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at [https://mozilla.org/MPL/2.0/](https://mozilla.org/MPL/2.0/).
