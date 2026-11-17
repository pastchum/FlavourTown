"""Recompute SIMILAR_TO edges from CONTAINS edges. Run after every ingestion."""

from __future__ import annotations

from .. import db
from ..config import settings
from .scoring import top_k_similar

FETCH = """
MATCH (i:Ingredient)-[:CONTAINS]->(c:Compound)
RETURN i.id AS id, collect(DISTINCT c.cid) AS cids
"""

CLEAR = "MATCH (:Ingredient)-[r:SIMILAR_TO]->(:Ingredient) DELETE r"

WRITE = """
UNWIND $rows AS row
MATCH (a:Ingredient {id: row.source}), (b:Ingredient {id: row.target})
MERGE (a)-[r:SIMILAR_TO]->(b)
SET r.score = row.score, r.shared_count = row.shared_count
"""


def run() -> int:
    ingredient_compounds = {row["id"]: set(row["cids"]) for row in db.read(FETCH)}
    edges = top_k_similar(ingredient_compounds, settings.similarity_top_k)
    rows = [
        {"source": a, "target": b, "score": score, "shared_count": shared}
        for a, b, score, shared in edges
    ]
    db.write(CLEAR)
    db.write(WRITE, rows=rows)
    return len(rows)


def main() -> None:
    print(f"Wrote {run()} SIMILAR_TO edges")
    db.close_driver()


if __name__ == "__main__":
    main()
