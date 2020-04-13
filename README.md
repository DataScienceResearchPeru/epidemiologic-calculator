# epidemiologic-calculator

## Installation

Make sure that you have installed Python 3.8.0 or later (https://www.python.org/).

It wil be better if you can handle your python versions with [pyenv](https://github.com/pyenv/pyenv)
and manage your dependencies with [poetry](https://github.com/python-poetry/poetry)

### Start project

Clone the project

```sh
git clone git@github.com:DataScienceResearchPeru/epidemiologic-calculator.git
```

Enter the project directory

```sh
 cd epidemiologic-calculator
```

Install all the dependencies
```sh
$ poetry install
```

Run project
```sh
$ poetry run python -m epical
```

Open the browser at http://127.0.0.1:8080/

### Development and code quality

To install code quality tools run the folowing commands

```
poetry run pre-commit install
```

Make your changes an stage them

```
git add .
```

Make your commit with poetry

```
poetry run git commit -m "your message here! :D"
```

I you have error, fix them an then repeat `git add .` and `poetry run git commit ...` and then

```
git push
```
