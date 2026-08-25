from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class GeneratedCase:
    public: dict
    private: dict
    canonical: dict
    content_hash: str
    phases: tuple[str, ...] = ()

    @property
    def bundle(self): return self.canonical
