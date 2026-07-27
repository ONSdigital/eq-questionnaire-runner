SCHEMAS_VERSION=`cat .schemas-version`
DESIGN_SYSTEM_VERSION=`cat .design-system-version`
RUNNER_ENV_FILE?=.development.env
SCHEMA_PATH=./schemas/test/en/

clean:
	find schemas/* -prune | grep -v "schemas/test" | xargs rm -r
	rm -rf templates/components
	rm -rf templates/layout

load-schemas:
	./scripts/load_release.sh onsdigital/census31-eq-questionnaire-schemas $(SCHEMAS_VERSION)

load-design-system-templates:
	./scripts/load_release.sh onsdigital/design-system $(DESIGN_SYSTEM_VERSION)
	./scripts/load_print_styles_from_cdn.sh $(DESIGN_SYSTEM_VERSION)

build: load-design-system-templates load-schemas translate

generate-pages:
	npm run generate_pages

lint-python:
	poetry run ./scripts/run_lint_python.sh

lint-test-python: lint-python test-unit

format-python:
	poetry run isort .
	poetry run black .

test:
	poetry run ./scripts/run_tests.sh

test-unit:
	poetry run ./scripts/run_tests_unit.sh

test-functional: generate-pages
	npm run test_functional

test-functional-headless: generate-pages
	EQ_RUN_FUNCTIONAL_TESTS_HEADLESS='True' make test-functional

test-functional-spec: generate-pages
	npm run test_functional -- --spec=./tests/functional/spec/$(SPEC)

test-functional-suite: generate-pages
	npm run test_functional -- --suite=$(SUITE)

generate-spec:
	poetry run python -m tests.functional.generate_pages \
		schemas/test/en/$(SCHEMA).json \
		./tests/functional/generated_pages/$(patsubst test_%,%,$(SCHEMA)) \
		-r '../../base_pages' \
		-s tests/functional/spec/$(SCHEMA).spec.js

validate-test-schemas:
	poetry run python -m scripts.validate_test_schemas

validate-test-schema:
	poetry run python -m scripts.validate_test_schemas $(SCHEMA_PATH)$(SCHEMA).json

translation-templates:
	poetry run python -m scripts.extract_translation_templates

test-translation-templates:
	poetry run python -m scripts.extract_translation_templates --test

translate:
	poetry run pybabel compile -d app/translations

run-validator:
	poetry run ./scripts/run_validator.sh

link-development-env:
	ln -sf $(RUNNER_ENV_FILE) .env

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
	docker compose -f docker-compose-dev.yml pull eq-questionnaire-launcher
	docker compose -f docker-compose-dev.yml up -d

dev-compose-down:
	docker compose -f docker-compose-dev.yml down

aims-compose-up:
	docker compose -f docker-compose-aims.yml up -d

aims-compose-down:
	docker compose -f docker-compose-aims.yml down

profile:
	poetry run python profile_application.py

generate-integration-test:
	poetry run python -m scripts.generate_integration_test
	poetry run black ./scripts/test_*

.PHONY: megalint megalint-apply clean-megalint
megalint:
	docker run --platform linux/amd64 --rm \
		-v /var/run/docker.sock:/var/run/docker.sock:rw \
		-v $(shell pwd):/tmp/lint:rw \
		ghcr.io/oxsecurity/megalinter:v9.6.0

megalint-apply:
	docker run --platform linux/amd64 --rm \
		-v /var/run/docker.sock:/var/run/docker.sock:rw \
		-v $(shell pwd):/tmp/lint:rw \
		-e APPLY_FIXES=all \
		ghcr.io/oxsecurity/megalinter:v9.6.0

clean-megalint:
	rm -rf megalinter-reports
