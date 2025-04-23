import networkx as nx
import random
import itertools

class SPSimulator:
    """
    Series–Parallel DAG generator simulating fork–join parallelism.
    Each node is annotated with:
      - 'thread': integer thread ID
      - 'var':    variable name (from `variables`)
      - 'op':     'R' or 'W' (read/write), with probability `p_write`

    Args:
      components:   number of initial base edges to combine
      p_series:     probability of choosing a series composition (vs. parallel)
      variables:    list of variable names (default ['x','y','z'])
      p_write:      probability an event is a write (default 0.3)
      seed:         optional int for reproducibility
    """
    def __init__(self,
                 components: int = 10,
                 p_series: float = 0.8,
                 variables: list[str] = ['u','v','w','x','y','z'],
                 p_write: float = 0.3,
                 seed: int = None):
        self.components = components
        self.p_series   = p_series
        self.variables  = variables
        self.p_write    = p_write

        if seed is not None:
            random.seed(seed)

        # for unique node IDs
        self._uid = itertools.count()
        # for assigning new thread IDs on fork
        self._thread_counter = itertools.count(1)
        # initial thread ID is 0

    def _new_node(self) -> str:
        return f"n{next(self._uid)}"

    def _make_event(self, node_id: str, thread_id: int):
        """Helper to create a node with read/write attributes."""
        op = 'W' if random.random() < self.p_write else 'R'
        var = random.choice(self.variables)
        return {'thread': thread_id, 'op': op, 'var': var}

    def _base(self):
        """
        Create the simplest SP component: two events in series on thread 0.
        Returns (G, s, t, nodes_set) where nodes_set = {s, t}.
        """
        G = nx.DiGraph()
        s, t = self._new_node(), self._new_node()
        # annotate both on thread 0
        G.add_node(s, **self._make_event(s, thread_id=0))
        G.add_node(t, **self._make_event(t, thread_id=0))
        G.add_edge(s, t)
        return (G, s, t, {s, t})

    def _series(self, comp1, comp2):
        """
        Series-compose two SP components by identifying comp1.t with comp2.s.
        Ensures no node has more than 2 children.
        """
        G1, s1, t1, nodes1 = comp1
        G2, s2, t2, nodes2 = comp2

        G = nx.DiGraph()
        # 1) copy G1
        for n in G1.nodes():
            G.add_node(n, **G1.nodes[n])
        G.add_edges_from(G1.edges())

        # 2) copy G2 with s2→t1 mapping
        mapping = {s2: t1}
        for n in G2.nodes():
            mapped = mapping.get(n, n)
            if mapped not in G:
                G.add_node(mapped, **G2.nodes[n])
        for u, v in G2.edges():
            u_m = mapping.get(u, u)
            v_m = mapping.get(v, v)
            # Ensure no node has more than 2 children
            if G.out_degree(u_m) < 2:
                G.add_edge(u_m, v_m)

        # merged node‐set
        mapped_nodes2 = {mapping.get(n, n) for n in nodes2}
        new_nodes = set(nodes1) | mapped_nodes2
        return (G, s1, t2, new_nodes)

    def _parallel(self, comp1, comp2):
        """
        Parallel-compose two SP components by forking comp2 onto a new thread,
        then joining both into new source & sink events.
        Ensures no node has more than 2 children.
        """
        G1, s1, t1, nodes1 = comp1
        G2, s2, t2, nodes2 = comp2

        # coordinator thread is the thread of comp1's source event
        coord_thread = G1.nodes[s1]['thread']
        # spawn a fresh thread for comp2's events
        new_thread = next(self._thread_counter)

        G = nx.DiGraph()
        new_s, new_t = self._new_node(), self._new_node()
        # annotate fork & join on coordinator thread
        G.add_node(new_s, **self._make_event(new_s, coord_thread))
        G.add_node(new_t, **self._make_event(new_t, coord_thread))

        # --- copy comp1: map s1→new_s, t1→new_t
        map1 = {s1: new_s, t1: new_t}
        for n in G1.nodes():
            mapped = map1.get(n, n)
            if mapped not in G:
                G.add_node(mapped, **G1.nodes[n])
        for u, v in G1.edges():
            if G.out_degree(map1.get(u, u)) < 2:
                G.add_edge(map1.get(u, u), map1.get(v, v))

        # --- copy comp2: map s2→new_s, t2→new_t, reassign thread=new_thread
        map2 = {s2: new_s, t2: new_t}
        for n in G2.nodes():
            mapped = map2.get(n, n)
            if mapped not in G:
                # copy attributes but override thread
                attrs = dict(G2.nodes[n])
                attrs['thread'] = new_thread
                G.add_node(mapped, **attrs)
        for u, v in G2.edges():
            if G.out_degree(map2.get(u, u)) < 2:
                G.add_edge(map2.get(u, u), map2.get(v, v))

        # build merged node‐set
        new_nodes = {
            map1.get(n, n) for n in nodes1
        } | {
            map2.get(n, n) for n in nodes2
        }

        return (G, new_s, new_t, new_nodes)

    def generate(self) -> nx.DiGraph:
        """
        Build one fork–join SP‐DAG by repeatedly series/parallel composing base components.
        """
        # start with a list of simple base components
        pool = [self._base() for _ in range(self.components + 1)]

        # combine until one SP graph remains
        while len(pool) > 1:
            comp1 = pool.pop(0)
            comp2 = pool.pop(0)
            if random.random() < self.p_series:
                new_comp = self._series(comp1, comp2)
            else:
                new_comp = self._parallel(comp1, comp2)
            pool.append(new_comp)

        # return just the graph
        G, _, _, _ = pool[0]
        return G

    @staticmethod
    def print_graph(G: nx.DiGraph):
        """Print each node with (thread,var,op) and all edges."""
        print("Nodes:")
        for n, attrs in G.nodes(data=True):
            print(f"  {n}: thread={attrs['thread']}, var={attrs['var']}, op={attrs['op']}, "
                  f"in={G.in_degree(n)}, out={G.out_degree(n)}")
        print("\nEdges:")
        for u, v in G.edges():
            print(f"  {u} → {v}")


if __name__ == '__main__':
    sim = SPSimulator(
        components=10,
        p_series=0.6,
        variables=['x','y','z','w'],
        p_write=0.4
    )
    sp_fj_dag = sim.generate()
    SPSimulator.print_graph(sp_fj_dag)
