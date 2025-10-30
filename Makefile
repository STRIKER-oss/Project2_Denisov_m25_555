install:
	poetry install

run:
	poetry run python -m src.primitive_db.main

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl
clean:
	rm -rf dist
	rm -rf .ruff_cache

test:
	poetry run python -m src.primitive_db.main
project:
	poetry run project
make lint:
	 poetry run ruff check .
 
