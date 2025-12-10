#!/bin/bash

# Skrypt do uruchamiania testów

cd "$(dirname "$0")"

# Tworzymy folder draw jeśli nie istnieje
mkdir -p draw

# Uruchamiamy testy przez poetry
poetry run pytest -v
