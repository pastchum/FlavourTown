"""Name clean-up and entity resolution across sources."""

from __future__ import annotations

import re

from .models import Dataset


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def normalize_descriptor(term: str) -> str:
    return term.strip().lower()


def merge(datasets: list[Dataset]) -> Dataset:
    """Merge sources into one dataset.

    Compounds merge on CID. Ingredients merge on id.
    TODO: resolve ingredient aliases through a curated table (data/aliases.csv) so that
    "tomato" and "tomato, raw" from different sources land on the same node.
    """
    compounds = {}
    ingredients = {}
    for ds in datasets:
        for c in ds.compounds:
            c.descriptors = sorted({normalize_descriptor(d) for d in c.descriptors})
            if c.cid in compounds:
                existing = compounds[c.cid]
                existing.descriptors = sorted(set(existing.descriptors) | set(c.descriptors))
                existing.smiles = existing.smiles or c.smiles
            else:
                compounds[c.cid] = c
        for i in ds.ingredients:
            if i.id in ingredients:
                existing = ingredients[i.id]
                existing.contains.extend(i.contains)
                existing.aliases = sorted(set(existing.aliases) | set(i.aliases))
                existing.category = existing.category or i.category
            else:
                ingredients[i.id] = i
    return Dataset(ingredients=list(ingredients.values()), compounds=list(compounds.values()))
