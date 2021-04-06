set -eu

rm -rf dist/* wscraper.egg-info/* && python setup.py sdist && twine upload dist/* -r $1
