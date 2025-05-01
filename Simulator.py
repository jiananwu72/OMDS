import random
import networkx as nx

def make_random_sp_dag(N,
                       p_series: float = 0.5,
                       p_read: float = 0.5,
                       var_pool=None):
    """
    Generate a random series‐parallel DAG with N leaves.
    
    Each step picks one existing leaf at random, replaces it
    with an S- or P-node, and gives that node two new leaves.
    
    Args:
      N         : total number of leaves desired (>=1)
      p_series  : probability of choosing an S-node (vs P-node)
      p_read    : probability that a new leaf is a read (“R”)
      var_pool  : list of variable names, e.g. ['x','y','z']
    Returns:
      G : networkx.DiGraph with exactly N leaves
    """
    if var_pool is None:
        var_pool = ['x','y','z']
    if N < 1:
        raise ValueError("N must be at least 1")
    
    G = nx.DiGraph()
    parent = {} 
    
    leaf_ctr = 1
    int_ctr  = 1
    
    u = f"u{leaf_ctr}"
    leaf_ctr += 1
    op = 'R' if random.random() < p_read else 'W'
    var = random.choice(var_pool)
    G.add_node(u, op=op, var=var, children=None)
    parent[u] = None
    leaves = [u]
    
    for _ in range(N-1):
        leaf = random.choice(leaves)
        leaves.remove(leaf)
        old_par = parent[leaf]
        
        kind = 'S' if random.random() < p_series else 'P'
        blk = f"{kind}{int_ctr}"
        int_ctr += 1
        
        left = f"u{leaf_ctr}"
        leaf_ctr += 1
        opL = 'R' if random.random() < p_read else 'W'
        varL = random.choice(var_pool)
        
        right = f"u{leaf_ctr}"
        leaf_ctr += 1
        opR = 'R' if random.random() < p_read else 'W'
        varR = random.choice(var_pool)
        
        G.add_node(blk, op=None, var=None, children=[left, right])
        parent[blk] = old_par
        
        G.add_node(left,  op=opL, var=varL, children=None)
        G.add_node(right, op=opR, var=varR, children=None)
        parent[left]  = blk
        parent[right] = blk
        leaves.extend([left, right])
        
        G.add_edge(blk, left)
        G.add_edge(blk, right)
        
        if old_par is None:
            pass
        else:
            ch = G.nodes[old_par]['children']
            ch[ch.index(leaf)] = blk
            G.nodes[old_par]['children'] = ch
            
            G.remove_edge(old_par, leaf)
            G.add_edge(old_par, blk)
        
        G.remove_node(leaf)
    
    return G

if __name__ == "__main__":
    # random.seed(0)
    G = make_random_sp_dag(5, p_series=0.6, p_read=0.7, var_pool=['x','y'])
    
    # print nodes in the same style as your example:
    for n, d in G.nodes(data=True):
        print(f'G.add_node("{n}", op={d["op"]!r}, var={d["var"]!r}, children={d["children"]})')
    print()
    for u, v in G.edges():
        print(f'G.add_edge("{u}", "{v}")')