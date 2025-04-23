import time
import itertools
import networkx as nx

from OrderMaintenance import OrderMaintenance
from OrderMaintenanceNaive import OrderMaintenanceNaive
from SPRaceDetector import SPRaceDetector
from SimpleSimulator import make_race_dag, make_no_race_dag


def naive_sp_race_detection(detector, G):
    """
    Perform naive SP-based race detection using detector.sp_precedes.
    Returns list of conflicting pairs.
    """
    # Collect event nodes (those with op 'R' or 'W')
    events = [n for n, d in G.nodes(data=True) if d.get('op') in ('R', 'W')]
    races = []
    for u, v in itertools.combinations(events, 2):
        du = G.nodes[u]
        dv = G.nodes[v]
        # same variable and at least one write
        if du['var'] == dv['var'] and ('W' in (du['op'], dv['op'])):
            # unordered in happens-before per SP detector
            if not detector.sp_precedes(u, v) and not detector.sp_precedes(v, u):
                races.append((u, v))
    return races


def test_performance():
    graphs = [
        ('Race', make_race_dag()),
        ('NoRace', make_no_race_dag()),
    ]
    om_variants = [
        ('NaiveOM', OrderMaintenanceNaive),
        ('OM', OrderMaintenance),
    ]

    for graph_name, G in graphs:
        print(f"\n=== Testing on {graph_name} DAG ===")
        # SP order build requires knowing root (assumed 'P1')
        root = 'P1'
        for om_name, om_class in om_variants:
            detector = SPRaceDetector(G, om_class)
            # Build the SP order structure
            detector.sp_order(root)
            # Time the naive race check using sp_precedes
            start = time.time()
            races = naive_sp_race_detection(detector, G)
            elapsed = time.time() - start
            print(f"{om_name}: found {len(races)} races in {elapsed:.6f} seconds")

def print_dag(G):
    print("Nodes:")
    for n, d in G.nodes(data=True):
        print(f"  {n}: op={d['op']}, var={d['var']}")
    print("\nEdges:")
    for u, v in G.edges():
        print(f"  {u} -> {v}")

if __name__ == '__main__':
    test_performance()
