![build status](https://github.com/dqd/big-five/actions/workflows/build.yml/badge.svg) ![coverage](./coverage.svg)

# Big Five personality traits
A source code of the [big-five.cz](https://big-five.cz/) website that provides personality traits test Big Five. Based on the [IPIP-NEO-PI](https://github.com/kholia/IPIP-NEO-PI) project, version 21.06.

Developed using [Django](https://www.djangoproject.com/) and [Vanilla JS](http://vanilla-js.com/).

## Installation
The project runs on port 9200, so you just visit the [http://localhost:9200/](http://localhost:9200/) URL after setting it up.

The installation itself is pretty straightforward on Unix-like systems:

1. Install [Docker](https://www.docker.com/) on your machine.
2. For a local development, copy the `docker-compose.override.yml-sample` file to `docker-compose.override.yml` and modify accordingly.
3. Apply migrations using the `./run.sh migrate` command.
4. Run it using the `docker compose up` command.

In production, you can use the provided `deploy.sh` script. And you will probably need to set your webserver to serve static files from the `bigfive/static` directory.

## Translation to other languages
The translation strings are located in the `.po` files. See [the Django documentation](https://docs.djangoproject.com/en/stable/topics/i18n/translation/) for details.
