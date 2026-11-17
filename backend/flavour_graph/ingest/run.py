"""Entry point: python -m flavour_graph.ingest.run [source ...]"""

from __future__ import annotations

import sys

from .. import db, schema
from ..similarity import job as similarity_job
from . import load as loader
from . import normalize
from .sources import flavordb, sample

SOURCES = {"sample": sample, "flavordb": flavordb}


def main() -> None:
    names = sys.argv[1:] or ["sample"]
    unknown = [n for n in names if n not in SOURCES]
    if unknown:
        sys.exit(f"Unknown source(s): {unknown}. Available: {sorted(SOURCES)}")

    schema.apply_schema()
    dataset = normalize.merge([SOURCES[n].load() for n in names])
    loader.load(dataset)
    print(f"Loaded {len(dataset.ingredients)} ingredients, {len(dataset.compounds)} compounds")

    written = similarity_job.run()
    print(f"Wrote {written} SIMILAR_TO edges")
    db.close_driver()


if __name__ == "__main__":
    main()
