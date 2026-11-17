"""Graph schema: constraints and indexes.

Nodes:  (:Ingredient {id, name, aliases})   (:Compound {cid, name, smiles, ingredient_count})
        (:Descriptor {name})                (:Category {name})
Edges:  (:Ingredient)-[:CONTAINS {concentration, unit, source}]->(:Compound)
        (:Compound)-[:HAS_DESCRIPTOR]->(:Descriptor)
        (:Ingredient)-[:IN_CATEGORY]->(:Category)
        (:Ingredient)-[:SIMILAR_TO {score, shared_count}]->(:Ingredient)   derived, see similarity/
"""

from . import db

STATEMENTS = [
    "CREATE CONSTRAINT ingredient_id IF NOT EXISTS FOR (i:Ingredient) REQUIRE i.id IS UNIQUE",
    "CREATE CONSTRAINT compound_cid IF NOT EXISTS FOR (c:Compound) REQUIRE c.cid IS UNIQUE",
    "CREATE CONSTRAINT descriptor_name IF NOT EXISTS FOR (d:Descriptor) REQUIRE d.name IS UNIQUE",
    "CREATE CONSTRAINT category_name IF NOT EXISTS FOR (c:Category) REQUIRE c.name IS UNIQUE",
    (
        "CREATE FULLTEXT INDEX entity_search IF NOT EXISTS "
        "FOR (n:Ingredient|Compound) ON EACH [n.name, n.aliases]"
    ),
]


def apply_schema() -> None:
    for statement in STATEMENTS:
        db.write(statement)
