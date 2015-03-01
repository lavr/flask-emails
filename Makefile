
clean:
	find . -name '*.pyc'  -exec rm -f {} \;
	find . -name '*.py~'  -exec rm -f {} \;
	rm -rf build dist *.egg-info

test:
	tox

upload:
	python setup.py sdist bdist_wheel upload
