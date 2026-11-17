from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .. import db
from . import queries


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    db.close_driver()


app = FastAPI(title="Flavour Graph API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/search")
def search(q: str = Query(min_length=1), limit: int = Query(10, le=50)) -> list[dict]:
    # Lucene prefix match on the last term; strip characters with special meaning.
    cleaned = "".join(ch for ch in q if ch.isalnum() or ch.isspace()).strip()
    if not cleaned:
        return []
    return db.read(queries.SEARCH, q=cleaned + "*", limit=limit)


@app.get("/ingredients/{ingredient_id}")
def ingredient(ingredient_id: str) -> dict:
    rows = db.read(queries.INGREDIENT, id=ingredient_id)
    if not rows:
        raise HTTPException(404, "Ingredient not found")
    return rows[0]


@app.get("/ingredients/{ingredient_id}/similar")
def similar(ingredient_id: str, limit: int = Query(25, le=100)) -> list[dict]:
    return db.read(queries.SIMILAR, id=ingredient_id, limit=limit)


@app.get("/ingredients/{a}/shared/{b}")
def shared(a: str, b: str) -> list[dict]:
    """The compounds two ingredients share: the 'why' behind a match."""
    return db.read(queries.SHARED, a=a, b=b)


@app.get("/graph/neighborhood")
def neighborhood(id: str, limit: int = Query(25, le=100)) -> dict:
    """Nodes and edges around one ingredient, shaped for the graph view."""
    rows = db.read(queries.SIMILAR, id=id, limit=limit)
    centre = db.read(queries.INGREDIENT, id=id)
    if not centre:
        raise HTTPException(404, "Ingredient not found")
    nodes = [{"id": id, "name": centre[0]["name"], "category": centre[0]["category"]}]
    nodes += [{"id": r["id"], "name": r["name"], "category": r["category"]} for r in rows]
    edges = [
        {"source": id, "target": r["id"], "score": r["score"], "shared_count": r["shared_count"]}
        for r in rows
    ]
    return {"nodes": nodes, "edges": edges}
