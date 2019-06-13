commands:
	@echo "test"
	@echo "install"
	@echo "build"
	@echo "upload"
	@echo "clean"
	@echo "release"

test:  clean
	python -m unittest tests

clean:
	find . -name '*.pyc' -exec rm -f {} +
# 	find . -name '*.pyo' -exec rm -f {} +
# 	find . -name '__pycache__' -exec rm -fr {} +
# 	rm -fr build/
# 	rm -fr dist/
# 	rm -fr *.egg-info
# 	find . -name '*~' -exec rm -f {} +