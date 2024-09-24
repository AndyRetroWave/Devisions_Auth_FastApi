PYTHON = python
UVI = uvicorn
RUFF = ruff
POETRY = poetry

.PHONY: run
run:
	$(UVI) main:app --reload

lint:
	$(RUFF) check .

git-commit:
	git add .
	git commit -m "update"
	git push

install:
	$(POETRY) shell
	$(POETRY) install

test:
	pytest