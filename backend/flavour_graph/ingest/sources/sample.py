"""Reads data/sample/sample.json. A tiny hand-made dataset to exercise the pipeline end to end.

Real adapters (flavordb.py, foodb.py) follow the same shape: fetch raw files into
data/raw/<source>/, then parse them into a Dataset.
"""

from __future__ import annotations

import json

from ...config import settings
from ..models import CompoundRecord, ContainsRecord, Dataset, IngredientRecord

SOURCE = "sample"


def load() -> Dataset:
    raw = json.loads((settings.data_dir / "sample" / "sample.json").read_text())
    compounds = [CompoundRecord(**c) for c in raw["compounds"]]
    ingredients = [
        IngredientRecord(
            id=i["id"],
            name=i["name"],
            category=i.get("category"),
            aliases=i.get("aliases", []),
            contains=[ContainsRecord(cid=cid, source=SOURCE) for cid in i["compounds"]],
        )
        for i in raw["ingredients"]
    ]
    return Dataset(ingredients=ingredients, compounds=compounds)
