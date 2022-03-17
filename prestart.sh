#! /usr/bin/env bash

sleep 10

poetry run alembic upgrade head
