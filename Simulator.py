import random
import networkx as nx

class Node:
    def __init__(self, kind, children=None, leaf_id=None):
        """
        kind: 'S' (series), 'P' (parallel), or 'leaf'
        children: list of child Nodes (only for 'S'/'P')
        leaf_id: integer id (only for 'leaf')
        """
        self.kind = kind
        self.children = children or []
        self.leaf_id = leaf_id
        self.parent = None
        for c in self.children:
            c.parent = self

    def __repr__(self):
        if self.kind == 'leaf':
            return f"Leaf({self.leaf_id})"
        return f"{self.kind}-node"

def generate_random_sp(N, p_series=0.5):
    """
    Build a random SP parse tree with exactly N leaves.
    
    Each step picks one existing leaf at random, replaces it
    with an S- or P-node, and gives that node two brand-new leaves.
    
    Args:
      N         : total number of leaves desired (must be ≥1)
      p_series  : probability of choosing an S-node (vs P-node)
    
    Returns:
      root node of the generated tree
    """
    if N < 1:
        raise ValueError("N must be at least 1")
    
    # start with a single leaf
    leaf_counter = 1
    root = Node('leaf', leaf_id=leaf_counter)
    leaf_counter += 1
    
    leaves = [root]
    
    # each expansion increases leaf count by +1; do exactly N-1 expansions
    for _ in range(N - 1):
        leaf = random.choice(leaves)
        
        # decide series vs parallel
        kind = 'S' if random.random() < p_series else 'P'
        
        # create two new leaves
        left  = Node('leaf', leaf_id=leaf_counter)
        leaf_counter += 1
        right = Node('leaf', leaf_id=leaf_counter)
        leaf_counter += 1
        
        # new internal node
        internal = Node(kind, children=[left, right])
        
        # splice internal into the tree in place of `leaf`
        if leaf.parent is None:
            root = internal
        else:
            parent = leaf.parent
            # replace leaf in its parent's children
            for idx, c in enumerate(parent.children):
                if c is leaf:
                    parent.children[idx] = internal
                    internal.parent = parent
                    break
        
        # update our leaf list
        leaves.remove(leaf)
        leaves.extend([left, right])
    
    return root

def print_sp_tree(node, indent=0):
    """Recursively print the tree structure."""
    prefix = " " * indent
    if node.kind == 'leaf':
        print(f"{prefix}Leaf(thread={node.leaf_id})")
    else:
        print(f"{prefix}{node.kind}-node")
        for child in node.children:
            print_sp_tree(child, indent + 2)

# ──────────────── Demo ────────────────
if __name__ == "__main__":
    random.seed(41)
    T = generate_random_sp(N=8, p_series=0.6)
    print_sp_tree(T)
