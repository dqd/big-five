![build status](https://github.com/dqd/big-five/actions/workflows/build.yml/badge.svg) ![coverage](./coverage.svg)

# Big Five personality traits
The source code of the [big-five.cz](https://big-five.cz/) website, which offers a free Big Five personality test. The questionnaire and its scoring are based on the [IPIP-NEO-PI](https://github.com/kholia/IPIP-NEO-PI) project, version 21.06, a Python port of John A. Johnson’s IPIP-NEO-120.

Developed using [Django](https://www.djangoproject.com/), [Pico CSS](https://picocss.com/), [Chart.js](https://www.chartjs.org/) and vanilla JavaScript.

## Installation
The project runs on port 9200, so you can visit [http://localhost:9200/](http://localhost:9200/) after setting it up.

The installation is straightforward on Unix-like systems:

1. Install [Docker](https://www.docker.com/) on your machine.
2. For local development, copy the `docker-compose.override.yml-sample` file to `docker-compose.override.yml` and modify it as needed.
3. Apply migrations using the `./run.sh migrate` command.
4. Run it using the `docker compose up` command.

In production, you can use the provided `deploy.sh` script. Set the `SECRET_KEY` environment variable to a long random string, and set up your web server to serve static files from the `bigfive/static` directory.

## Development
The `run.sh` script runs Django management commands inside the container, for example:

```sh
./run.sh test              # run the tests
./run.sh coverage          # run the tests and print the coverage report
./run.sh makemigrations    # create migrations after changing the models
```

The code is formatted and linted by [Ruff](https://docs.astral.sh/ruff/). Install [pre-commit](https://pre-commit.com/) and run `pre-commit install` to have it checked before every commit.

## Translation to other languages
The translation strings are located in the `.po` files in the `bigfive/locale` directory. To update them after changing the texts, run:

```sh
./run.sh makemessages --all
./run.sh compilemessages
```

See [the Django documentation](https://docs.djangoproject.com/en/stable/topics/i18n/translation/) for details.
