SCHEMAS_VERSION=`cat .schemas-version`
DESIGN_SYSTEM_VERSION=`cat .design-system-version`
RUNNER_ENV_FILE?=.development.env
SCHEMA_PATH=./schemas/test/en/

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

generate-pages:
	npm run generate_pages

lint: lint-python lint-js

lint-python:
	pipenv run ./scripts/run_lint_python.sh

lint-test-python: lint-python test-unit

format: format-python format-js

format-python:
	pipenv run isort .
	pipenv run black .

test:
	pipenv run ./scripts/run_tests.sh

test-unit:
	pipenv run ./scripts/run_tests_unit.sh

test-functional: generate-pages
	npm run test_functional

test-functional-headless: generate-pages
	EQ_RUN_FUNCTIONAL_TESTS_HEADLESS='True' make test-functional

test-functional-spec: generate-pages
	npm run test_functional -- --spec=./tests/functional/spec/$(SPEC)

test-functional-suite: generate-pages
	npm run test_functional -- --suite=$(SUITE)

lint-js:
	npm run lint

format-js:
	npm run format

generate-spec:
	pipenv run python -m tests.functional.generate_pages schemas/test/en/$(SCHEMA).json ./tests/functional/generated_pages/$(patsubst test_%,%,$(SCHEMA)) -r '../../base_pages' -s tests/functional/spec/$(SCHEMA).spec.js

validate-test-schemas:
	./scripts/validate_test_schemas.sh

validate-test-schema:
	./scripts/validate_test_schemas.sh $(SCHEMA_PATH)$(SCHEMA).json

translation-templates:
	pipenv run python -m scripts.extract_translation_templates

test-translation-templates:
	pipenv run python -m scripts.extract_translation_templates --test

translate:
	pipenv run pybabel compile -d app/translations

run-validator:
	pipenv run ./scripts/run_validator.sh

link-development-env:
	ln -sf $(RUNNER_ENV_FILE) .env

run: build link-development-env
	pipenv run flask run

run-gunicorn-async: link-development-env
	WEB_SERVER_TYPE=gunicorn-async pipenv run ./run_app.sh

run-gunicorn-threads: link-development-env
	WEB_SERVER_TYPE=gunicorn-threads pipenv run ./run_app.sh

run-uwsgi: link-development-env
	WEB_SERVER_TYPE=uwsgi pipenv run ./run_app.sh

run-uwsgi-threads: link-development-env
	WEB_SERVER_TYPE=uwsgi-threads pipenv run ./run_app.sh

run-uwsgi-async: link-development-env
	WEB_SERVER_TYPE=uwsgi-async pipenv run ./run_app.sh

dev-compose-up:
	docker-compose -f docker-compose-dev-mac.yml pull eq-questionnaire-launcher
	docker-compose -f docker-compose-dev-mac.yml pull sds
	docker-compose -f docker-compose-dev-mac.yml pull cir
	docker-compose -f docker-compose-dev-mac.yml up -d

dev-compose-up-linux:
	docker-compose -f docker-compose-dev-linux.yml up -d

dev-compose-down:
	docker-compose -f docker-compose-dev-mac.yml down

dev-compose-down-linux:
	docker-compose -f docker-compose-dev-linux.yml down

profile:
	pipenv run python profile_application.py

generate-integration-test:
	pipenv run playwright install chromium
	pipenv run python -m scripts.generate_integration_test
	pipenv run black ./scripts/test_*
