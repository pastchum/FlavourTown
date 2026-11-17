"""Idempotent upserts into Neo4j."""

from __future__ import annotations

from dataclasses import asdict

from .. import db
from .models import Dataset

UPSERT_COMPOUNDS = """
UNWIND $rows AS row
MERGE (c:Compound {cid: row.cid})
SET c.name = row.name, c.smiles = row.smiles
WITH c, row
UNWIND row.descriptors AS descriptor
MERGE (d:Descriptor {name: descriptor})
MERGE (c)-[:HAS_DESCRIPTOR]->(d)
"""

UPSERT_INGREDIENTS = """
UNWIND $rows AS row
MERGE (i:Ingredient {id: row.id})
SET i.name = row.name, i.aliases = row.aliases
FOREACH (_ IN CASE WHEN row.category IS NULL THEN [] ELSE [1] END |
  MERGE (cat:Category {name: row.category})
  MERGE (i)-[:IN_CATEGORY]->(cat))
WITH i, row
UNWIND row.contains AS edge
MATCH (c:Compound {cid: edge.cid})
MERGE (i)-[r:CONTAINS {source: edge.source}]->(c)
SET r.concentration = edge.concentration, r.unit = edge.unit
"""

UPDATE_INGREDIENT_COUNTS = """
MATCH (c:Compound)
SET c.ingredient_count = COUNT { (c)<-[:CONTAINS]-(:Ingredient) }
"""


def load(dataset: Dataset) -> None:
    db.write(UPSERT_COMPOUNDS, rows=[asdict(c) for c in dataset.compounds])
    db.write(UPSERT_INGREDIENTS, rows=[asdict(i) for i in dataset.ingredients])
    db.write(UPDATE_INGREDIENT_COUNTS)
