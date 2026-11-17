"use client";

import cytoscape from "cytoscape";
import { useEffect, useRef } from "react";
import type { Neighborhood } from "@/lib/api";

const CATEGORY_COLORS: Record<string, string> = {
  fruit: "#e11d48",
  vegetable: "#16a34a",
  herb: "#0d9488",
  spice: "#d97706",
  dairy: "#2563eb",
};

type Props = {
  graph: Neighborhood;
  centreId: string;
  onSelect: (id: string) => void;
};

export function GraphView({ graph, centreId, onSelect }: Props) {
  const container = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!container.current) return;
    const cy = cytoscape({
      container: container.current,
      elements: [
        ...graph.nodes.map((n) => ({
          data: {
            id: n.id,
            label: n.name,
            color: CATEGORY_COLORS[n.category ?? ""] ?? "#71717a",
            size: n.id === centreId ? 44 : 28,
          },
        })),
        ...graph.edges.map((e) => ({
          data: {
            id: `${e.source}->${e.target}`,
            source: e.source,
            target: e.target,
            width: 1 + e.score * 6,
          },
        })),
      ],
      style: [
        {
          selector: "node",
          style: {
            label: "data(label)",
            "background-color": "data(color)",
            width: "data(size)",
            height: "data(size)",
            "font-size": 12,
            color: "#71717a",
            "text-margin-y": -6,
          },
        },
        {
          selector: "edge",
          style: {
            width: "data(width)",
            "line-color": "#a1a1aa",
            opacity: 0.6,
          },
        },
      ],
      layout: { name: "concentric", minNodeSpacing: 40 },
    });
    cy.on("tap", "node", (event) => onSelect(event.target.id()));
    return () => cy.destroy();
  }, [graph, centreId, onSelect]);

  return <div ref={container} className="h-full w-full" />;
}
