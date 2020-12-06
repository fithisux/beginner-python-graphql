#!/bin/sh

export FLASK_ENV=development
export FLASK_APP=flaskql
flask init-db
flask run