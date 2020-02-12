clean:
	rm -rf schemas
	rm -rf templates/components
	rm -rf templates/layout

load-schemas:
	./scripts/load_release.sh onsdigital/eq-questionnaire-schemas v0.0.3

load-templates:
	./scripts/load_release.sh onsdigital/design-system 14.4.7

build: load-templates
	make translate

lint:
	pipenv run ./scripts/run_lint_python.sh

test:
	pipenv run ./scripts/run_tests.sh

test-unit:
	pipenv run ./scripts/run_tests_unit.sh

test-functional:
	pipenv run ./scripts/run_tests_functional.sh

validate-test-schemas:
	pipenv run ./scripts/validate_test_schemas.sh

translation-templates:
	pipenv run python -m scripts.extract_translation_templates

test-translation-templates:
	pipenv run python -m scripts.extract_translation_templates --test

translate:
	pipenv run pybabel compile -d app/translations

run-validator:
	pipenv run ./scripts/run_validator.sh

run: build
	ln -sf .development.env .env
	pipenv run flask run

gunicorn:
	ln -sf .development.env .env
	pipenv run ./run_gunicorn.sh

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
	pipenv run python profile_application.py
