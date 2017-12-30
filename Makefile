test:
	git checkout master
	git pull
	tox

doc:
	git checkout gh-pages
	rm -rf docs _sources _static
	git checkout psilva/docs docs
	git reset HEAD
	cd docs; make html
	mv -fv docs/build/html/* ./
	rm -rf docs
	git add -A
	git commit -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`"
	git push origin gh-pages
	git checkout psilva/docs

release: test
	bumpversion minor
	python setup.py bdist_wheel upload
	bumpversion --no-tag patch
	git push origin master --tags

.PHONY: test doc release
