.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[1m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: lint
lint: ## Run mypy
	mypy -m libpalette.scripts.main

.PHONY: test
test: ## Run a sanity test
	python3 -m libpalette.scripts.main -c examples/simple-example.yml --backend none --socket /tmp/test_palette_socket --verbose

.PHONY: build
build: ## Build the .whl file
	python3 -m build

.PHONY: install
install: ## Install the .whl file
	python3 -m pip install --force-reinstall dist/commandpalette*.whl

.PHONY: upload
upload: ## Upload to pypi
	python3 -m twine upload dist/*

.PHONY: build-docs
build-docs: ## Generate manpage
	pandoc -s -t man docs/manpage.md -o docs/palette.1

.PHONY: install-docs
install-docs: ## Install manpage
	sudo bash -c "cat docs/palette.1 | gzip > /usr/local/man/man1/palette.1"
	sudo bash -c "ln -f /usr/local/man/man1/palette.1 /usr/local/man/man1/paletted.1"

.PHONY: clean
clean: ## Clean generated files
	-rm -rf dist palette.egg-info/ .mypy_cache/ dist/ __pycache__/