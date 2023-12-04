#!/bin/sh

if [ "$1" = "coverage" ]
then
    docker compose run --rm bigfive sh -c 'coverage run --data-file=/tmp/.coverage manage.py test && coverage report --data-file=/tmp/.coverage'
else
    docker compose run --rm bigfive python ./manage.py $*
fi
