.PHONY: test check build

test:
	python -m unittest discover -s tests -p 'test_*.py'

check:
	python -m py_compile removebgvideo/*.py

build:
	python -m build
