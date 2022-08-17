# Format source code automatically
style:
	black --line-length 119 --target-version py37 src/cer
	isort src/cer

# Control quality
quality:
	black --check --line-length 119 --target-version py37 src/cer
	isort --check-only src/cer
	flake8 src/cer --exclude __pycache__,__init__.py

# Run tests
test:
	pytest tests
