
upload_pypi:
	rm -rf build dist msbench.egg-info
	python setup.py sdist bdist_wheel
	twine upload --repository pypi dist/*