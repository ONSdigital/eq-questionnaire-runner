SCHEMAS_VERSION=`cat .schemas-version`
DESIGN_SYSTEM_VERSION=`cat .design-system-version`

clean:
	find schemas/* -prune | grep -v "schemas/test" | xargs rm -r
	rm -rf templates/components
	rm -rf templates/layout

load-schemas:
	./scripts/load_release.sh onsdigital/eq-questionnaire-schemas $(SCHEMAS_VERSION)

load-design-system-templates:
	./scripts/load_release.sh onsdigital/design-system $(DESIGN_SYSTEM_VERSION)
	./scripts/load_print_styles_from_cdn.sh $(DESIGN_SYSTEM_VERSION)

build: load-design-system-templates load-schemas translate

lint: lint-python
	yarn lint

lint-python:
	poetry run ./scripts/run_lint_python.sh

format: format-python
	yarn format

format-python:
	poetry run isort .
	poetry run black .

test:
	poetry run ./scripts/run_tests.sh

test-unit:
	poetry run ./scripts/run_tests_unit.sh

test-functional:
	poetry run ./scripts/run_tests_functional.sh

validate-test-schemas:
	poetry run ./scripts/validate_test_schemas.sh

translation-templates:
	poetry run python -m scripts.extract_translation_templates

test-translation-templates:
	poetry run python -m scripts.extract_translation_templates --test

translate:
	poetry run pybabel compile -d app/translations

run-validator:
	poetry run ./scripts/run_validator.sh

link-development-env:
	ln -sf .development.env .env

run: build link-development-env
	poetry run flask run

run-gunicorn-async: link-development-env
	WEB_SERVER_TYPE=gunicorn-async poetry run ./run_app.sh

run-gunicorn-threads: link-development-env
	WEB_SERVER_TYPE=gunicorn-threads poetry run ./run_app.sh

run-uwsgi: link-development-env
	WEB_SERVER_TYPE=uwsgi poetry run ./run_app.sh

run-uwsgi-threads: link-development-env
	WEB_SERVER_TYPE=uwsgi-threads poetry run ./run_app.sh

run-uwsgi-async: link-development-env
	WEB_SERVER_TYPE=uwsgi-async poetry run ./run_app.sh

dev-compose-up:
	docker-compose pull eq-questionnaire-launcher
	docker-compose -f docker-compose-dev-mac.yml up -d

dev-compose-up-linux:
	docker-compose -f docker-compose-dev-linux.yml up -d

dev-compose-down:
	docker-compose -f docker-compose-dev-mac.yml down

dev-compose-down-linux:
	docker-compose -f docker-compose-dev-linux.yml down

profile:
	poetry run python profile_application.py
