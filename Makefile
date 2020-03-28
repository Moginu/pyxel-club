.DEFAULT_GOAL := help
PIPENV_RUN := pipenv run

help:  ## print this help
	@# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""
.PHONY: help

run:  ## Run game
		$(PIPENV_RUN) python src/app.py
.PHONY: run

edit:  ## Run editor
		$(PIPENV_RUN) pyxeleditor src/assets/jump_game.pyxres
.PHONY: editor

flake8:  ## Check flake8
		$(PIPENV_RUN) flake8 src/app.py
.PHONY: flake8
