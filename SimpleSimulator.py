import networkx as nx

def make_race_dag():
    G = nx.DiGraph()

    G.add_node("P1", op=None, var=None, children=["S1", "S3"])

    G.add_node("S1", op=None, var=None, children=["u1", "S2"])
    G.add_node("u1", op="R", var="x", children=None)
    G.add_node("S2", op=None, var=None, children=["P2", "u4"])
    G.add_node("u4", op=None, var=None, children=None)
    G.add_node("P2", op=None, var=None, children=["u2", "u3"])
    G.add_node("u2", op=None, var=None, children=None)
    G.add_node("u3", op="W", var="x", children=None)

    G.add_node("S3", op=None, var=None, children=["u5", "S4"])
    G.add_node("u5", op="R", var="x", children=None)
    G.add_node("S4", op=None, var=None, children=["P3", "u8"])
    G.add_node("u8", op="R", var="x", children=None)
    G.add_node("P3", op=None, var=None, children=["u6", "u7"])
    G.add_node("u6", op=None, var=None, children=None)
    G.add_node("u7", op=None, var=None, children=None)

    G.add_edge("P1", "S1")
    G.add_edge("P1", "S3")

    G.add_edge("S1", "u1")
    G.add_edge("S1", "S2")
    G.add_edge("S2", "P2")
    G.add_edge("S2", "u4")
    G.add_edge("P2", "u2")
    G.add_edge("P2", "u3")

    G.add_edge("S3", "u5")
    G.add_edge("S3", "S4")
    G.add_edge("S4", "P3")
    G.add_edge("S4", "u8")
    G.add_edge("P3", "u6")
    G.add_edge("P3", "u7")

    return G

def make_no_race_dag():
    G = nx.DiGraph()

    G.add_node("P1", op=None, var=None, children=["S1", "S3"])

    G.add_node("S1", op=None, var=None, children=["u1", "S2"])
    G.add_node("u1", op="R", var="x", children=None)
    G.add_node("S2", op=None, var=None, children=["P2", "u4"])
    G.add_node("u4", op=None, var=None, children=None)
    G.add_node("P2", op=None, var=None, children=["u2", "u3"])
    G.add_node("u2", op=None, var=None, children=None)
    G.add_node("u3", op="W", var="x")

    G.add_node("S3", op=None, var=None, children=["u5", "S4"])
    G.add_node("u5", op="R", var="y", children=None)
    G.add_node("S4", op=None, var=None, children=["P3", "u8"])
    G.add_node("u8", op="R", var="y", children=None)
    G.add_node("P3", op=None, var=None, children=["u6", "u7"])
    G.add_node("u6", op="W", var="y", children=None)
    G.add_node("u7", op=None, var=None, children=None)

    G.add_edge("P1", "S1")
    G.add_edge("P1", "S3")

    G.add_edge("S1", "u1")
    G.add_edge("S1", "S2")
    G.add_edge("S2", "P2")
    G.add_edge("S2", "u4")
    G.add_edge("P2", "u2")
    G.add_edge("P2", "u3")

    G.add_edge("S3", "u5")
    G.add_edge("S3", "S4")
    G.add_edge("S4", "P3")
    G.add_edge("S4", "u8")
    G.add_edge("P3", "u6")
    G.add_edge("P3", "u7")

    return G

def print_dag(G):
    print("Nodes:")
    for n, d in G.nodes(data=True):
        print(f"  {n}: op={d['op']}, var={d['var']}")
    print("\nEdges:")
    for u, v in G.edges():
        print(f"  {u} -> {v}")

if __name__ == "__main__":
    race_dag    = make_race_dag()
    no_race_dag = make_no_race_dag()

    print("=== Race DAG ===")
    print_dag(race_dag)

    print("\n=== No-Race DAG ===")
    print_dag(no_race_dag)
