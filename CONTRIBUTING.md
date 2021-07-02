<!-- This Source Code Form is subject to the terms of the Mozilla Public
   - License, v. 2.0. If a copy of the MPL was not distributed with this
   - file, You can obtain one at https://mozilla.org/MPL/2.0/. -->

## Contributing

[fork]: https://github.com/kennylajara/RunUp/fork  
[pr]: https://github.com/kennylajara/RunUp/compare  
[code-of-conduct]: CODE_OF_CONDUCT.md
[mpl-headers]: https://www.mozilla.org/en-US/MPL/headers/

Hi there! We're thrilled that you'd like to contribute to this project. Your help is essential for keeping it great.

Contributions to this project are released to the public under the [Mozilla Public License Version 2.0](https://runup.readthedocs.io/en/latest/license/).

Please note that this project is released with a [Contributor Code of Conduct][code-of-conduct]. By participating in this project you agree to abide by its terms.

## Submitting a pull request

1. [Fork][fork] and clone the repository
1. Configure and install the dependencies: `python3 -m pip install -r requirements-dev.txt`
1. Install the editable RunUp package: `python3 -m pip install --editable .` 
1. Create a new branch: `git checkout -b my-branch-name`
1. Make your change
1. Add [MPL 2 headers][mpl-headers] at the top of any new file created or modified file, if missing.
1. Format the modified files with Black: `black .`
1. Use Flake8 to look for additional format errors so you can fix them (manually): `flake8 .`
1. Commit the changes
1. Push to your fork and [submit a pull request][pr]

After that, you can pat your self on the back and wait for your pull request to be reviewed and merged.

Here are a few things you can do that will increase the likelihood of your pull request being accepted:
- Keep your change as focused as possible. If there are multiple changes you would like to make that are not dependent upon each other, consider submitting them as separate pull requests.
- Write a [good commit message](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).

## Resources

- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [Using Pull Requests](https://help.github.com/articles/about-pull-requests/)
