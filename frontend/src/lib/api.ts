const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type SearchResult = {
  type: "Ingredient" | "Compound";
  id: string;
  name: string;
  score: number;
};

export type GraphNode = { id: string; name: string; category: string | null };
export type GraphEdge = {
  source: string;
  target: string;
  score: number;
  shared_count: number;
};
export type Neighborhood = { nodes: GraphNode[]; edges: GraphEdge[] };

export type SharedCompound = {
  cid: number;
  name: string;
  ingredient_count: number;
  descriptors: string[];
};

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API_URL}${path}`);
  if (!res.ok) throw new Error(`API ${res.status} for ${path}`);
  return res.json();
}

export const api = {
  search: (q: string) =>
    get<SearchResult[]>(`/search?q=${encodeURIComponent(q)}`),
  neighborhood: (id: string) =>
    get<Neighborhood>(`/graph/neighborhood?id=${encodeURIComponent(id)}`),
  shared: (a: string, b: string) =>
    get<SharedCompound[]>(
      `/ingredients/${encodeURIComponent(a)}/shared/${encodeURIComponent(b)}`,
    ),
};
