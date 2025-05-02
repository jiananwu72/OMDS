import networkx as nx
from itertools import combinations

def naive_race_detection(detector, G):
    """
    Naive baseline race detector.
    
    Args:
      G: networkx.DiGraph whose nodes have attributes
         - 'op'  in {'R','W',None}
         - 'var' in {<varname>, None}
    
    Returns:
      List of tuples (u, v) of leaf-node IDs that race.
    """
    events = [
        n for n,d in G.nodes(data=True)
        if d.get('op') in ('R','W')
    ]

    races = []
    for u, v in combinations(events, 2):
        du, dv = G.nodes[u], G.nodes[v]

        # same var & at least one write?
        if du['var'] != dv['var']:
            continue
        if du['op'] == 'R' and dv['op'] == 'R':
            continue

        # neither precedes the other in G
        if not nx.has_path(G, u, v) and not nx.has_path(G, v, u):
            races.append((u, v))

    return races