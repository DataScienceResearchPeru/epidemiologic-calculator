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
$ FLASK_APP=epidemicalk poetry run flask database migrate
$ FLASK_APP=epidemicalk poetry run flask database load_fixtures
$ poetry run python -m epidemicalk
```

Open the browser at `http://127.0.0.1:8080/`

### Start project with docker

Create `.env` and `.env.db` files according to the examples in `.env.template`. Then run the folowing `docker-compose` commands

```
$ docker-compose build
$ docker-compose run -e FLASK_APP=epidemicalk --rm web flask database migrate
$ docker-compose run -e FLASK_APP=epidemicalk --rm web flask database load_fixtures
$ docker-compose up
```

Open the browser at `http://127.0.0.1:8000/`

## Development and code quality

To install code quality tools run the folowing commands

```
$ poetry run pre-commit install
```

Make your changes an stage them

```
$ git add .
```

Make your commit with poetry

```
$ poetry run git commit -m "your message here! :D"
```

I you have error, fix them an then repeat `git add .` and `poetry run git commit ...`. If there are no errors then

```
$ git push
```
