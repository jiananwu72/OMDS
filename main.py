import time
import itertools
import networkx as nx

from OrderMaintenance import OrderMaintenance
from OrderMaintenanceNaive import OrderMaintenanceNaive
from SPRaceDetector import SPRaceDetector, sp_race_detection
from NaiveRaceDetector import naive_race_detection
from Simulator import make_random_sp_dag

def test_performance(G):
    om_variants = [
        ('NaiveOM', OrderMaintenanceNaive),
        ('OM', OrderMaintenance),
    ]
    detection_methods = [
        ('naive', naive_race_detection),
        ('sp',    sp_race_detection),
    ]

    root = next(iter(G.nodes))
    for om_name, om_class in om_variants:
        # for the SP‐based method we need to build the SP‐order once
        detector = SPRaceDetector(G, om_class)
        detector.sp_order(root)

        for method_name, func in detection_methods:
            start = time.time()
            races = func(detector, G)

            elapsed = time.time() - start
            print(f"{om_name}-{method_name:5s}: "
                  f"found {len(races):4d} races in {elapsed:.6f}s")

def print_dag(G):
    print("Nodes:")
    for n, d in G.nodes(data=True):
        print(f"  {n}: op={d['op']}, var={d['var']}")
    print("\nEdges:")
    for u, v in G.edges():
        print(f"  {u} -> {v}")

if __name__ == '__main__':
    G = make_random_sp_dag(1500, p_series=0.3, p_read=0.7, var_pool=['a','b','c','d','e','f','g','h'])
    test_performance(G)
