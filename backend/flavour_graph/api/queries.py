"""All Cypher the API runs. Parameterised; the frontend never sends Cypher."""

SEARCH = """
CALL db.index.fulltext.queryNodes('entity_search', $q) YIELD node, score
RETURN labels(node)[0] AS type,
       coalesce(node.id, toString(node.cid)) AS id,
       node.name AS name,
       score
ORDER BY score DESC
LIMIT $limit
"""

INGREDIENT = """
MATCH (i:Ingredient {id: $id})
OPTIONAL MATCH (i)-[:IN_CATEGORY]->(cat:Category)
CALL (i) {
  MATCH (i)-[:CONTAINS]->(c:Compound)
  OPTIONAL MATCH (c)-[:HAS_DESCRIPTOR]->(d:Descriptor)
  WITH c, collect(d.name) AS descriptors
  RETURN collect({cid: c.cid, name: c.name, descriptors: descriptors}) AS compounds
}
RETURN i.id AS id, i.name AS name, i.aliases AS aliases, cat.name AS category, compounds
"""

SIMILAR = """
MATCH (:Ingredient {id: $id})-[r:SIMILAR_TO]->(other:Ingredient)
OPTIONAL MATCH (other)-[:IN_CATEGORY]->(cat:Category)
RETURN other.id AS id, other.name AS name, cat.name AS category,
       r.score AS score, r.shared_count AS shared_count
ORDER BY r.score DESC
LIMIT $limit
"""

SHARED = """
MATCH (:Ingredient {id: $a})-[:CONTAINS]->(c:Compound)<-[:CONTAINS]-(:Ingredient {id: $b})
OPTIONAL MATCH (c)-[:HAS_DESCRIPTOR]->(d:Descriptor)
RETURN c.cid AS cid, c.name AS name, c.ingredient_count AS ingredient_count,
       collect(d.name) AS descriptors
ORDER BY c.ingredient_count ASC
"""
