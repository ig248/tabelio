
## Development installation
```bash
pyenv install 3.6.4
pyenv virtualenv 3.6.4 tabelio
pyenv activate tabelio
pip install -r requirements-dev.txt
pip install -e .
```

## Run lint checks

```bash
make lint
```

## Run unit tests

```bash
make lint
```

## Release instructions

1. Merge your changes into `master` branch.
2. Pull the latest master on your machine.
2. Create pypi config file on your machine (`~/.pypirc`).

```
...
```

4. Update `HISTORY.rst` with a description of the changes in this release, and edit the unreleased version number depending on your changes. Do not change `(unreleased)` manually, the next step will do this for you.

Use Semantic Versioning (not sure what that is? read https://semver.org/):

>> MAJOR version when you make incompatible API changes,
>> MINOR version when you add functionality in a backwards-compatible manner, and
>> PATCH version when you make backwards-compatible bug fixes.
>> Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.

5. Run `fullrelease` to begin the release process. Follow the questions CAREFULLY, it will attempt to get the version from HISTORY.rst, but be sure to double check the release version it suggests to you in the terminal.

Once the release wizard is complete you should be able to `pip install table-convert`.
