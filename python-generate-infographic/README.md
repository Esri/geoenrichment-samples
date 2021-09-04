# python-generate-infographic

Example for generating Esri Infogrpahics using Python.

## Getting Started

1 - Clone this repo.

2 - Create an environment with the requirements.
    
```
        > make env
```

3 - Explore - After the environment is created and acivated, type `jupyter lab` in the root of the project, and look in the `./notebooks` directory.

## Using Make - common commands

Based on the pattern provided in the [Cookiecutter Data Science template by Driven Data](https://drivendata.github.io/cookiecutter-data-science/) this template streamlines a number of commands using the `make` command pattern.

- `make env` - builds the Conda environment with all the name and dependencies from `environment_dev.yml` and installs the local project package `generate_infographic` using the command `python -m pip install -e ./src/src/generate_infographic` so you can easily test against the package as you are developing it.

- `make docs` - builds Sphinx docs based on files in `./docsrc/source` and places them in `./docs`. This enables easy publishing in the master branch in GitHub.

- `make test` - activates the environment created by the `make env` or `make env_clone` and runs all the tests in the `./testing` directory using PyTest. Alternately, if you prefer to use [TOX](https://tox.readthedocs.io) for testing (my preference), there is a `tox.ini` file included as well. The dependencies (`tox` and `tox-conda`) for using TOX are included in the default requirements.

<p><small>Project based on the <a target="_blank" href="https://github.com/knu2xs/cookiecutter-geoai">cookiecutter GeoAI project template</a>. This template, in turn, is simply an extension and light modification of the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
