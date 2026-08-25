.PHONY: setup lint typecheck test-unit test-data test-contract test-e2e test-visual test-assets test-security test-a11y dependency-audit test-soak test-secondary-soak test-chaos test-web test-sql test-genie-live deploy-staging smoke-staging soak deployed-soak release-report release-gate audit-contract docker-build docker-smoke

setup:
	python -m pip install -e ".[dev]"

lint:
	python -m compileall -q server tests scripts

typecheck:
	python -m mypy server --ignore-missing-imports --follow-imports=skip --no-site-packages

test-unit:
	python -m pytest -q

test-data:
	python -m pytest -q tests/test_domain.py tests/test_mutation.py

test-contract:
	python -m pytest -q tests/test_case_contract.py

test-e2e:
	python scripts/local_e2e.py

test-visual: build
	python scripts/visual_gate.py

build:
	npm run build

test-assets:
	python scripts/release_check.py
	python scripts/assets_gate.py

test-security:
	python scripts/security_gate.py

test-a11y:
	python scripts/a11y_gate.py

dependency-audit:
	npm audit --omit=dev --audit-level=high

test-soak:
	python scripts/local_soak.py

test-secondary-soak:
	python scripts/local_secondary_soak.py

test-chaos:
	python scripts/local_chaos.py

test-sql:
	python scripts/live_sql_check.py

test-genie-live:
	python scripts/live_genie_check.py

release-report:
	python scripts/release_gate.py

deploy-staging:
	@test -n "$(DATABRICKS_SOURCE_PATH)" || (echo "DATABRICKS_SOURCE_PATH is required" && exit 1)
	databricks workspace import-dir . "$(DATABRICKS_SOURCE_PATH)" --overwrite -p sda
	databricks apps deploy mad-data-lab --source-code-path "$(DATABRICKS_SOURCE_PATH)" -p sda

smoke-staging:
	python scripts/deployed_smoke.py

deployed-soak:
	python -u scripts/deployed_soak.py

soak: deployed-soak

test-web:
	python scripts/local_web_smoke.py

release-gate: lint typecheck test-unit test-data test-contract build test-e2e test-visual test-assets test-security test-a11y dependency-audit test-soak test-chaos

audit-contract:
	python scripts/validate_mdl2_contract.py --strict

docker-smoke: docker-build
	docker compose up -d
	python scripts/container_smoke.py
	python scripts/container_shutdown_smoke.py
	docker compose down

docker-build:
	docker build -t mad-data-lab:local .
