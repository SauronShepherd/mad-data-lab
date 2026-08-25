class PrivateTruthRepository:
    """Deployment-only oracle boundary; never imported by the public API."""
    def __init__(self, loader): self._loader = loader
    def get(self, case_id: str): return self._loader(case_id)
