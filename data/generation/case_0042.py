"""Named Case #042 generator entry point for release and validation tooling."""

from .generator import FORMULA, FORMULA_HASH, PHASES, generate_case

CASE_ID = "CASE_0042"
PRODUCTION_SEED = 42

__all__ = ["CASE_ID", "FORMULA", "FORMULA_HASH", "PHASES", "PRODUCTION_SEED", "generate_case"]
