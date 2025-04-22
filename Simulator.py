import networkx as nx
import random

class Simulator:
    """
    Simulator for generating a happens‑before DAG with read/write events for race detection.

    Args:
      num_threads: number of threads (each has a linear program of events)
      events_per_thread: number of events each thread executes
      variables: list of variable names (default ['x', 'y', 'z'])
      p_write: probability an event is a write (default 0.3)
      p_hb: probability of adding a cross‑thread happens‑before edge (default 0.1)
      seed: optional int for reproducible randomness
    """
    def __init__(self,
                 num_threads=2,
                 events_per_thread=10,
                 variables=None,
                 p_write=0.3,
                 p_hb=0.1,
                 seed=None):
        self.num_threads = num_threads
        self.events_per_thread = events_per_thread
        self.variables = variables or ['x', 'y', 'z']
        self.p_write = p_write
        self.p_hb = p_hb
        if seed is not None:
            random.seed(seed)
        self.dag = nx.DiGraph()
        # Random thread ordering to avoid cycles in cross edges
        order = list(range(self.num_threads))
        random.shuffle(order)
        self.thread_rank = {t: rank for rank, t in enumerate(order)}

    def generate(self) -> nx.DiGraph:
        """
        Build the DAG:
        - Each thread has sequential edges between its events.
        - Cross‑thread edges are added probabilistically in one direction to maintain acyclicity.
        Returns:
          A networkx.DiGraph with nodes labeled by 'thread', 'var', and 'op'.
        """
        # Create events and thread‑local happens‑before edges
        for t in range(self.num_threads):
            prev = None
            for i in range(self.events_per_thread):
                node_id = f"t{t}_e{i}"
                op = 'W' if random.random() < self.p_write else 'R'
                var = random.choice(self.variables)
                self.dag.add_node(node_id,
                                  thread=t,
                                  var=var,
                                  op=op)
                if prev:
                    self.dag.add_edge(prev, node_id)
                prev = node_id

        # Add cross‑thread happens‑before edges
        nodes = list(self.dag.nodes())
        for u in nodes:
            for v in nodes:
                if u == v:
                    continue
                t_u = self.dag.nodes[u]['thread']
                t_v = self.dag.nodes[v]['thread']
                # only between different threads
                if t_u == t_v:
                    continue
                # direct only from lower‑rank to higher‑rank thread
                if self.thread_rank[t_u] < self.thread_rank[t_v]:
                    if random.random() < self.p_hb:
                        self.dag.add_edge(u, v)
        return self.dag

if __name__ == '__main__':
    # Demo
    sim = Simulator(num_threads=3,
                    events_per_thread=5,
                    seed=42)
    dag = sim.generate()
    print("Nodes and attributes:")
    for n, attrs in dag.nodes(data=True):
        print(f" {n}: thread={attrs['thread']}, var={attrs['var']}, op={attrs['op']}")
    print("\nEdges (happens-before):")
    for u, v in dag.edges():
        print(f" {u} -> {v}")
