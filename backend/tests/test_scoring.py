from flavour_graph.similarity.scoring import idf_weights, top_k_similar, weighted_jaccard


def test_rare_shared_compound_outweighs_common_one():
    data = {
        "a": {1, 2},
        "b": {1, 2},  # shares rare compound 2 with a
        "c": {1, 3},  # shares only ubiquitous compound 1 with a
        "d": {1, 4},
    }
    weights = idf_weights(data)
    assert weights[2] > weights[1]
    assert weighted_jaccard(data["a"], data["b"], weights) > weighted_jaccard(
        data["a"], data["c"], weights
    )


def test_top_k_limits_and_orders():
    data = {"a": {1, 2}, "b": {1, 2}, "c": {1, 3}, "d": {9}}
    edges = top_k_similar(data, k=1)
    assert ("a", "b", 1.0, 2) in edges
    assert all(e[0] != "d" for e in edges)  # no shared compounds, no edges
    assert len([e for e in edges if e[0] == "a"]) == 1
