test:
	git checkout master
	git pull
	tox

doc:
	git checkout gh-pages
	rm -rf build _sources _static
	git checkout master $(GH_PAGES_SOURCES)
	git reset HEAD
	make html
	mv -fv build/html/* ./
	rm -rf $(GH_PAGES_SOURCES) build
	git add -A
	git ci -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`" && git push origin gh-pages ; git checkout master

release: test
	bumpversion minor
	python setup.py bdist_wheel upload
	bumpversion --no-tag patch
	git push origin master --tags

.PHONY: test doc release
