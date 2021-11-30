ALL: black

black:
	black --check . --target-version py37 --diff --line-length 120 --skip-string-normalization

clean:
	@find . -name '*.pyc' -delete
	@find . -name __pycache__  -type d | xargs rm -rf
	@echo "cleaned up"

cov: clean
	pytest -v tests/ --cov=one_puzzle

test: clean
	pytest -v tests/
