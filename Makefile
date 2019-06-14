ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

commands:
	@echo "test"
	@echo "install"
	@echo "setup-venv"
	@echo "build-upload"
	@echo "build"
	@echo "upload"
	@echo "clean"
	@echo "release"

install: setup-venv
	@echo "start install"

setup-venv:
	@echo "$(ROOT_DIR)/env"
	if ! [ -d "$(ROOT_DIR)/env" ]; then python -m venv env; fi;

test:  clean
	python -m unittest tests

clean:
	find . -name '*.pyc' -exec rm -f {} +
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
# 	find . -name '*.pyo' -exec rm -f {} +
# 	find . -name '__pycache__' -exec rm -fr {} +
# 	find . -name '*~' -exec rm -f {} +

build-upload: build upload clean

build: clean
	python $(ROOT_DIR)/setup.py sdist bdist_wheel
upload:
	python -m twine upload dist/*
