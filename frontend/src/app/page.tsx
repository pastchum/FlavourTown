"use client";

import { useCallback, useEffect, useState } from "react";
import { GraphView } from "@/components/GraphView";
import {
  api,
  type Neighborhood,
  type SearchResult,
  type SharedCompound,
} from "@/lib/api";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [centreId, setCentreId] = useState<string | null>(null);
  const [graph, setGraph] = useState<Neighborhood | null>(null);
  const [compare, setCompare] = useState<{
    id: string;
    compounds: SharedCompound[];
  } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!query.trim()) return;
    const timer = setTimeout(() => {
      api
        .search(query)
        .then((rows) => setResults(rows.filter((r) => r.type === "Ingredient")))
        .catch((e) => setError(String(e)));
    }, 200);
    return () => clearTimeout(timer);
  }, [query]);

  const select = useCallback((id: string) => {
    setError(null);
    setCompare(null);
    setResults([]);
    setCentreId(id);
    api
      .neighborhood(id)
      .then(setGraph)
      .catch((e) => setError(String(e)));
  }, []);

  const showShared = (otherId: string) => {
    if (!centreId) return;
    api
      .shared(centreId, otherId)
      .then((compounds) => setCompare({ id: otherId, compounds }))
      .catch((e) => setError(String(e)));
  };

  const nameOf = (id: string) =>
    graph?.nodes.find((n) => n.id === id)?.name ?? id;

  return (
    <div className="flex h-screen flex-col">
      <header className="flex items-center gap-4 border-b border-zinc-200 px-6 py-3 dark:border-zinc-800">
        <h1 className="font-semibold">Flavour Graph</h1>
        <div className="relative w-80">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search an ingredient"
            className="w-full rounded border border-zinc-300 bg-transparent px-3 py-1.5 text-sm dark:border-zinc-700"
          />
          {query.trim() && results.length > 0 && (
            <ul className="absolute z-10 mt-1 w-full rounded border border-zinc-200 bg-white text-sm shadow dark:border-zinc-700 dark:bg-zinc-900">
              {results.map((r) => (
                <li key={r.id}>
                  <button
                    onClick={() => select(r.id)}
                    className="w-full px-3 py-1.5 text-left hover:bg-zinc-100 dark:hover:bg-zinc-800"
                  >
                    {r.name}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
      </header>

      <div className="flex min-h-0 flex-1">
        <main className="min-w-0 flex-1">
          {graph && centreId ? (
            <GraphView graph={graph} centreId={centreId} onSelect={select} />
          ) : (
            <p className="p-6 text-sm text-zinc-500">
              Search for an ingredient to see what it tastes similar to.
            </p>
          )}
        </main>

        {graph && centreId && (
          <aside className="w-80 overflow-y-auto border-l border-zinc-200 p-4 text-sm dark:border-zinc-800">
            <h2 className="mb-2 font-semibold">
              Similar to {nameOf(centreId)}
            </h2>
            <ul>
              {graph.edges.map((e) => (
                <li key={e.target}>
                  <button
                    onClick={() => showShared(e.target)}
                    className="flex w-full justify-between rounded px-2 py-1 hover:bg-zinc-100 dark:hover:bg-zinc-800"
                  >
                    <span>{nameOf(e.target)}</span>
                    <span className="tabular-nums text-zinc-500">
                      {e.score.toFixed(2)}
                    </span>
                  </button>
                </li>
              ))}
            </ul>

            {compare && (
              <>
                <h2 className="mb-2 mt-6 font-semibold">
                  Shared with {nameOf(compare.id)}
                </h2>
                <ul className="space-y-2">
                  {compare.compounds.map((c) => (
                    <li key={c.cid}>
                      <div>{c.name}</div>
                      <div className="text-zinc-500">
                        {c.descriptors.join(", ")}
                      </div>
                    </li>
                  ))}
                </ul>
              </>
            )}
          </aside>
        )}
      </div>
    </div>
  );
}
