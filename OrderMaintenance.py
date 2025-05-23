class OMNode:
    """
    A node in the order‑maintenance list.
    Each node has:
      - val:     the user‑stored value
      - label:   an integer that determines its position
      - prev:    pointer to previous node
      - next:    pointer to next node
    """
    __slots__ = ('val', 'label', 'prev', 'next')

    def __init__(self, val, label):
        self.val = val
        self.label = label
        self.prev = None
        self.next = None

    def __repr__(self):
        return f"OMNode(val={self.val!r}, label={self.label})"


class OrderMaintenance:
    """
    Order‑maintenance data structure using integer labels + doubly linked list.
    - Order queries are label comparisons: O(1) worst‑case.
    - Insertions/deletions are O(1) amortized: occasional local relabeling
      of a small block restores gaps between labels.
    """

    def __init__(self, initial_gap=1 << 20, bucket_size=100):
        """
        initial_gap: starting gap between adjacent labels
        block_size:  max number of nodes to relabel in one rebalance
        """
        self.head = None
        self.tail = None
        self.gap = initial_gap
        self.bucket_size = bucket_size

    def insert_after(self, node, val):
        """
        Insert new element with value `val` immediately after `node`.
        If node is None, insert at the front.
        Returns the newly created OMNode.
        """
        # Empty list or insert at front
        if node is None:
            if self.head is None:
                # First element in list
                new_label = 0
                new_node = OMNode(val, new_label)
                self.head = self.tail = new_node
                return new_node
            else:
                # Insert before current head
                next_node = self.head
                new_label = next_node.label - self.gap
                new_node = OMNode(val, new_label)
                new_node.next = next_node
                next_node.prev = new_node
                self.head = new_node
                return new_node

        # Insert after a real node
        next_node = node.next
        if next_node is None:
            # Insert at end
            new_label = node.label + self.gap
            new_node = OMNode(val, new_label)
            node.next = new_node
            new_node.prev = node
            self.tail = new_node
            return new_node

        # Insert in between node and next_node
        if next_node.label - node.label > 1:
            # Enough numeric space: pick midpoint
            new_label = (node.label + next_node.label) // 2
        else:
            # Gap exhausted: relabel a small block starting at node
            self._relabel_block(node)
            # Now there is room
            new_label = (node.label + next_node.label) // 2

        # Splice in new node
        new_node = OMNode(val, new_label)
        new_node.prev = node
        new_node.next = next_node
        node.next = new_node
        next_node.prev = new_node
        return new_node

    def _relabel_block(self, node):
        """
        Relabel up to `block size` nodes starting at start_node (micro‑bucket).
        Ensures monotonic labels with new small gaps within the bucket.
        """
        # Collect a small bucket of nodes
        nodes = []
        curr = node
        for _ in range(self.bucket_size):
            if curr is None:
                break
            nodes.append(curr)
            curr = curr.next

        # Need at least two nodes to rebalance
        if len(nodes) < 2:
            return

        after = curr  # first node after bucket, could be None
        L = nodes[0].label
        if after and after.label > L:
            R = after.label
        else:
            # No room after bucket: create artificial macro gap
            R = L + self.bucket_size * self.gap * 2

        k = len(nodes)
        delta = (R - L) // (k + 1)
        if delta <= 0:
            delta = 1

        # Assign new micro‑labels evenly spaced in (L, R)
        label = L + delta
        for node in nodes:
            node.label = label
            label += delta

    def delete(self, node):
        """
        Remove `node` from the list.
        O(1) time (standard doubly‑linked‑list unlink).
        """
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        node.prev = node.next = None

    def comes_before(self, a, b):
        """
        Return True iff node a precedes node b in the list.
        O(1) label comparison.
        """
        return a.label < b.label

    def __iter__(self):
        """
        Iterate over nodes in order.
        """
        curr = self.head
        while curr:
            yield curr
            curr = curr.next

    def __repr__(self):
        vals = [f"{n.val!r}@{n.label}" for n in self]
        return "OM[" + " → ".join(vals) + "]"


if __name__ == "__main__":
    # --- Demo ---
    om = OrderMaintenance(initial_gap=100)

    # Build a simple list
    n0 = om.insert_after(None, "A")
    n1 = om.insert_after(n0, "B")
    n2 = om.insert_after(n1, "C")
    print("Initial:", om)

    # Insert between B and C
    n1_5 = om.insert_after(n1, "B.5")
    print("After inserting B.5:", om)

    # Force relabeling by inserting many in the same gap
    for i in range(6):
        om.insert_after(n1, f"X{i}")
    print("After crowding B's gap:", om)

    # Order queries
    print("A before C?", om.comes_before(n0, n2))
    print("C before B.5?", om.comes_before(n2, n1_5))

    # Deletion
    om.delete(n1_5)
    print("After deleting B.5:", om)
