"""FlavorDB adapter. TODO.

Plan:
1. fetch(): download entity JSON into data/raw/flavordb/ (skip files that already exist).
2. load(): parse the raw files into a Dataset, keyed on PubChem CID.
"""

from __future__ import annotations

from ..models import Dataset

SOURCE = "flavordb"


def load() -> Dataset:
    raise NotImplementedError("FlavorDB adapter not written yet")
