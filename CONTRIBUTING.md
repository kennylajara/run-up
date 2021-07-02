## Contributing

[fork]: https://github.com/kennylajara/RunUp/fork  
[pr]: https://github.com/kennylajara/RunUp/compare  
[code-of-conduct]: CODE_OF_CONDUCT.md  

Hi there! We're thrilled that you'd like to contribute to this project. Your help is essential for keeping it great.

Contributions to this project are released to the public under the [Mozilla Public License Version 2.0](https://runup.readthedocs.io/en/latest/license/).

Please note that this project is released with a [Contributor Code of Conduct][code-of-conduct]. By participating in this project you agree to abide by its terms.

## Submitting a pull request

0. [Fork][fork] and clone the repository
0. Configure and install the dependencies: `python3 -m pip install -r requirements-dev.txt`
0. Install the editable RunUp package: `python3 -m pip install --editable .` 
0. Create a new branch: `git checkout -b my-branch-name`
0. Make your change
0. Format the modified files with Black: `black .`
0. Look for any additional format errors with Flake8 `flake8 .` and fix it (manually).
0. Commit the changes
0. Push to your fork and [submit a pull request][pr]
0. Pat your self on the back and wait for your pull request to be reviewed and merged.

Here are a few things you can do that will increase the likelihood of your pull request being accepted:
- Keep your change as focused as possible. If there are multiple changes you would like to make that are not dependent upon each other, consider submitting them as separate pull requests.
- Write a [good commit message](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).

## Resources

- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [Using Pull Requests](https://help.github.com/articles/about-pull-requests/)
