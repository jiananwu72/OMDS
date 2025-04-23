import networkx as nx

def compile_to_hb(parseG):
    """
    parseG: your parse‐tree DiGraph, where each node has:
      - d['children'] = [left, right] or None
      - d['op'], d['var'] on leaves
    Returns: a new DiGraph Hb with real happens-before edges.
    """
    Hb = nx.DiGraph()
    thread_counter = 0
    # map parse-node → (thread_id, first_event, last_event)
    info = {}

    def dfs(u, thread_id):
        nonlocal thread_counter
        data = parseG.nodes[u]
        children = data.get('children')
        if not children:
            # leaf event
            Hb.add_node(u, op=data['op'], var=data['var'], thread=thread_id)
            # link from previous on that thread?
            prev = getattr(dfs, f"last_{thread_id}", None)
            if prev:
                Hb.add_edge(prev, u)
            setattr(dfs, f"last_{thread_id}", u)
            return u, u, thread_id

        # internal node: series or parallel?
        left, right = children
        kind = data.get('kind', 'P')  # you could store 'S'/'P' in parseG.nodes[u]['kind']
        if kind == 'S':
            # series: same thread
            first, last, _ = dfs(left, thread_id)
            return dfs(right, thread_id)  # links automatically in seq order
        else:
            # parallel: fork new thread for right subtree
            fork = f"fork_{u}"
            join = f"join_{u}"
            Hb.add_node(fork, op=None, var=None, thread=thread_id)
            prev = getattr(dfs, f"last_{thread_id}", None)
            if prev:
                Hb.add_edge(prev, fork)
            # left branch on same thread
            L_first, L_last, _ = dfs(left, thread_id)
            # right branch gets new id
            thread_counter += 1
            new_t = thread_counter
            R_first, R_last, _ = dfs(right, new_t)
            # emit join
            Hb.add_node(join, op=None, var=None, thread=thread_id)
            Hb.add_edge(L_last, join)
            Hb.add_edge(R_last, join)
            setattr(dfs, f"last_{thread_id}", join)
            return fork, join, thread_id

    # assume top‐node is “P1”
    dfs("P1", 0)
    return Hb

def naive_race_detector(Hb):
    races = []
    nodes = list(Hb.nodes(data=True))
    for i, (u, du) in enumerate(nodes):
        for v, dv in nodes[i+1:]:
            if du.get('var') == dv.get('var') \
               and ('W' in (du.get('op'), dv.get('op'))) \
               and not nx.has_path(Hb, u, v) \
               and not nx.has_path(Hb, v, u):
                races.append((u, v))
    return races

if __name__ == "__main__":
    from SimpleSimulator import make_race_dag, make_no_race_dag, print_dag

    parse = make_race_dag()
    Hb    = compile_to_hb(parse)
    print("Races:", naive_race_detector(Hb))

    parse = make_no_race_dag()
    Hb    = compile_to_hb(parse)
    print("Races:", naive_race_detector(Hb))
