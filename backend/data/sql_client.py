from __future__ import annotations

import os
import re
from contextlib import contextmanager

class SqlAdapterError(RuntimeError):
    """A platform/connection error, never a malformed evidence response."""

_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

def execute_native(cursor, sql: str, params: tuple | list = ()):
    """Execute only connector-native positional parameters; never interpolate."""
    if ":case_id" in sql or ":limit" in sql:
        raise ValueError("trusted SQL must use native positional parameters")
    return cursor.execute(sql, params)

def validate_case_id(case_id: str) -> str:
    if not re.fullmatch(r"CASE_[0-9]{4}", case_id): raise ValueError("invalid case_id")
    return case_id

def connection_options(environ: dict[str, str] | None = None) -> tuple[str, str, dict]:
    """Build connector options using Databricks OAuth, never an application PAT."""
    env = environ or os.environ
    host = env.get("DATABRICKS_SERVER_HOSTNAME") or env.get("DATABRICKS_HOST")
    http_path = env.get("DATABRICKS_HTTP_PATH")
    if not host or not http_path:
        raise SqlAdapterError("staging SQL resource binding is incomplete")
    host = host.removeprefix("https://")
    client_id, client_secret = env.get("DATABRICKS_CLIENT_ID"), env.get("DATABRICKS_CLIENT_SECRET")
    if client_id and client_secret:
        from databricks.sdk.core import Config, oauth_service_principal
        cfg = Config(host=f"https://{host}", client_id=client_id, client_secret=client_secret)
        return host, http_path, {"credentials_provider": lambda: oauth_service_principal(cfg)}
    return host, http_path, {"auth_type": "databricks-oauth"}

def configured_object(catalog: str, schema: str, object_name: str) -> str:
    if not all(_IDENTIFIER.fullmatch(v or '') for v in (catalog, schema, object_name)):
        raise ValueError("catalog/schema/object names are deployment configuration, not user input")
    return f"{catalog}.{schema}.{object_name}"

@contextmanager
def connect_from_env():
    """Connect using Databricks resource-bound environment variables on staging."""
    try:
        from databricks import sql
    except ImportError as exc:
        raise SqlAdapterError("databricks-sql-connector is not installed") from exc
    host, http_path, options = connection_options()
    try:
        with sql.connect(server_hostname=host, http_path=http_path, **options) as connection:
            yield connection
    except Exception as exc:
        raise SqlAdapterError("Databricks SQL connection failed") from exc
