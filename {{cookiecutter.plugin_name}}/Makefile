#!/usr/bin/make -f

SHELL=/bin/bash -o pipefail -o errexit -o nounset
.ONESHELL:  # for Python virtual environment
.PHONY: build-docker run-docker venv install run local-test

build-docker:
	curl --max-time 10 -sS -I https://pypi.dev.twilio.com/simple || { echo 'Please establish VPN connection for pip3 install'; exit 1; }
	docker build -t cloudquery-plugin-{{cookiecutter.plugin_name}}:latest .

run-docker:
	docker run -it --rm -p 7777:7777 cloudquery-plugin-{{cookiecutter.plugin_name}}:latest serve --address '[::]:7777' --log-format json --log-level debug

# target to create virtual environment
venv:
	python3 -m venv venv

install: venv  # target to install dependencies
	. venv/bin/activate
	pip install -i https://pypi.dev.twilio.com/simple/ -r requirements_poetry.txt
	poetry install
	cloudquery plugin install TestConfig.yaml

run: venv  # target to run script
	. venv/bin/activate
	python main.py serve --address [::]:7777 --log-level debug

local-test:
	cloudquery sync TestConfig.yaml
