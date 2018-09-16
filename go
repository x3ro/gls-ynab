#!/bin/bash

function ensure_venv {
	if [ ! -d "venv" ]; then
		virtualenv venv
		pip install -r requirements.txt
	fi
	source ./venv/bin/activate
}

function run {
	ensure_venv
	python3 gls-ynab.py "$@"
}

run "$@"