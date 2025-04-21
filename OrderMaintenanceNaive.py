class OMNaiveNode:
    """
    A node in the naive order‑maintenance list.
    Each node has:
      - val:     the user‑stored value
    """
    __slots__ = ('val',)
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f"OMNodeNaive({self.val!r})"


class OrderMaintenanceNaive:
    """
    Naive order‑maintenance using a Python list.
    All operations—insert, delete, and order‑query—take O(n) time.
    """
    def __init__(self):
        # internal list of OMNodeNaive instances, in order
        self._elems = []

    def insert_after(self, node, val):
        """
        Insert a new value `val` immediately after `node`.
        If node is None, insert at the front.
        Returns the new OMNodeNaive.
        Time: O(n) for list.insert or .index
        """
        new_node = OMNaiveNode(val)
        if node is None:
            # at front
            self._elems.insert(0, new_node)
        else:
            idx = self._elems.index(node)      # O(n)
            self._elems.insert(idx + 1, new_node)  # O(n)
        return new_node

    def delete(self, node):
        """
        Remove `node` from the sequence.
        Time: O(n) for list.remove
        """
        self._elems.remove(node)

    def comes_before(self, a, b):
        """
        Return True iff node a appears before node b.
        Time: O(n) for two .index calls
        """
        return self._elems.index(a) < self._elems.index(b)

    def __iter__(self):
        """Iterate over nodes in order."""
        return iter(self._elems)

    def __repr__(self):
        vals = [str(node.val) for node in self._elems]
        return "OMNaive[" + " → ".join(vals) + "]"


if __name__ == "__main__":
    om = OrderMaintenanceNaive()

    # build list: A, B, C
    nA = om.insert_after(None, "A")
    nB = om.insert_after(nA, "B")
    nC = om.insert_after(nB, "C")
    print("Initial:", om)

    # insert X between A and B
    nX = om.insert_after(nA, "X")
    print("After inserting X:", om)

    # order queries
    print("A before X?", om.comes_before(nA, nX))
    print("C before X?", om.comes_before(nC, nX))

    # delete B
    om.delete(nB)
    print("After deleting B:", om)
