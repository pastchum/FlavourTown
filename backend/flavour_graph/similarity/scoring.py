"""Pure scoring functions, no database access."""

from __future__ import annotations

import math
from collections import defaultdict


def idf_weights(ingredient_compounds: dict[str, set[int]]) -> dict[int, float]:
    """Rare compounds weigh more than ubiquitous ones."""
    n = len(ingredient_compounds)
    counts: dict[int, int] = defaultdict(int)
    for compounds in ingredient_compounds.values():
        for cid in compounds:
            counts[cid] += 1
    return {cid: math.log(1 + n / count) for cid, count in counts.items()}


def weighted_jaccard(a: set[int], b: set[int], weights: dict[int, float]) -> float:
    union = sum(weights[c] for c in a | b)
    if union == 0:
        return 0.0
    return sum(weights[c] for c in a & b) / union


def top_k_similar(
    ingredient_compounds: dict[str, set[int]], k: int
) -> list[tuple[str, str, float, int]]:
    """Return (source, target, score, shared_count) for each ingredient's k best matches.

    Brute-force over all pairs: fine for a few thousand ingredients.
    """
    weights = idf_weights(ingredient_compounds)
    ids = sorted(ingredient_compounds)
    edges = []
    for a in ids:
        scored = []
        for b in ids:
            if a == b:
                continue
            shared = len(ingredient_compounds[a] & ingredient_compounds[b])
            if shared:
                score = weighted_jaccard(ingredient_compounds[a], ingredient_compounds[b], weights)
                scored.append((a, b, score, shared))
        scored.sort(key=lambda e: e[2], reverse=True)
        edges.extend(scored[:k])
    return edges
