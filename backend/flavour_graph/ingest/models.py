"""Normalised records every source adapter must produce."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CompoundRecord:
    cid: int  # PubChem CID, the canonical key
    name: str
    smiles: Optional[str] = None
    descriptors: list[str] = field(default_factory=list)


@dataclass
class ContainsRecord:
    cid: int
    source: str
    concentration: Optional[float] = None
    unit: Optional[str] = None


@dataclass
class IngredientRecord:
    id: str  # stable slug, e.g. "strawberry"
    name: str
    category: Optional[str] = None
    aliases: list[str] = field(default_factory=list)
    contains: list[ContainsRecord] = field(default_factory=list)


@dataclass
class Dataset:
    ingredients: list[IngredientRecord] = field(default_factory=list)
    compounds: list[CompoundRecord] = field(default_factory=list)
