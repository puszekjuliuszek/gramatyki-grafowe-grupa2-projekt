#!/bin/bash

cd "$(dirname "$0")"
mkdir -p draw
poetry run pytest -v
