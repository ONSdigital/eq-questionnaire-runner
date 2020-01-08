clean:
	rm -rf schemas/en
	rm -rf schemas/cy
	rm -rf schemas/eo
	rm -rf schemas/ga

load-schemas:
	pipenv run ./scripts/load_schemas.sh

load-templates:
	pipenv run ./scripts/load_templates.sh

load:
	pipenv run ./scripts/load.sh

lint:
	pipenv run ./scripts/run_lint.sh

test:
	pipenv run ./scripts/run_tests.sh

test-unit:
	pipenv run ./scripts/run_tests_unit.sh

test-functional:
	pipenv run ./scripts/run_tests_functional.sh

test-schemas:
	pipenv run ./scripts/test_schemas.sh

run: load
	ln -sf .development.env .env
	pipenv run flask run

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

travis: clean
	ln -sf .development.env .env
	pipenv run ./scripts/run_travis.sh
