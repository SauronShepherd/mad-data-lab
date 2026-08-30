# MDL-2 platform verification

## Local verification

- Python tests: 45 passed.
- Vite `npm ci` and `npm run build`: passed.
- Docker image build/start smoke: passed.

## Databricks verification

The requested CLI profile `sda` was probed on 2026-08-24. It failed before any workspace or SQL operation because its refresh token is invalid. No remote mutation was attempted.

Required reauthentication command: `databricks auth login --profile sda`.
