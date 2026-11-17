# Flavour Knowledge Graph

A knowledge graph of ingredients and the flavour compounds they contain, with a similarity search and a graph explorer on top.

## Layout

```
backend/flavour_graph/
  schema.py        graph model: constraints and indexes
  ingest/          source adapters -> normalise -> upsert into Neo4j
  similarity/      derives SIMILAR_TO edges from CONTAINS edges
  api/             read-only FastAPI layer
frontend/          Next.js explorer (search, similar list, graph view)
data/sample/       tiny illustrative dataset
data/raw/          downloaded source snapshots (not committed)
```

## Graph model

```
(:Ingredient)-[:CONTAINS {concentration, unit, source}]->(:Compound)
(:Compound)-[:HAS_DESCRIPTOR]->(:Descriptor)
(:Ingredient)-[:IN_CATEGORY]->(:Category)
(:Ingredient)-[:SIMILAR_TO {score, shared_count}]->(:Ingredient)   # derived
```

## Run

```sh
cp .env.example .env
docker compose up -d                                              # Neo4j + API on :8000
docker compose exec backend python -m flavour_graph.ingest.run    # load sample data, compute similarity
cd frontend && npm run dev                                        # explorer on :3000
```

Neo4j browser: http://localhost:7474. API docs: http://localhost:8000/docs.

## Tests

```sh
cd backend && python3 -m venv .venv && .venv/bin/pip install -U pip && .venv/bin/pip install -e ".[dev]" && .venv/bin/pytest
```

## Next steps

- Write the FlavorDB adapter (`backend/flavour_graph/ingest/sources/flavordb.py`).
- Add a curated ingredient alias table for merging sources.
- Add FooDB concentrations and move scoring towards odor activity values.
