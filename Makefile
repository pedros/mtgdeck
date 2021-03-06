test:
	git checkout master
	git pull
	tox

doc:
	git checkout gh-pages
	rm -rf docs src _sources _static _build _modules
	git clean -dfx
	git checkout master docs src README.rst
	git reset HEAD
	sphinx-apidoc -o docs/source src/mtgdeck
	cd docs; make html
	mv -fv docs/build/html/* ./
	rm -rf docs src
	git add -A
	git commit -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`" && git push origin gh-pages ; git checkout master

release: test doc
	bumpversion minor
	python setup.py bdist_wheel upload
	bumpversion --no-tag patch
	git push origin master --tags

.PHONY: test doc release
