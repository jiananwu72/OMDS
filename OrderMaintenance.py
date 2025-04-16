class OrderMaintenance:
    def __init__(self):
        self.order = []
    
    def OM_INSERT(self, new_item, after_item=None):
        """
        Inserts new_item into the order immediately after after_item.
        If after_item is None, inserts at the beginning.
        """
        if after_item is None:
            # No reference provided; insert at the beginning.
            self.order.insert(0, new_item)
        else:
            try:
                idx = self.order.index(after_item)
            except ValueError:
                raise ValueError(f"OM_INSERT Error: The reference item '{after_item}' is not in the order.")
            self.order.insert(idx + 1, new_item)
        # For debugging purposes
        # print("Order after insertion:", self.order)

    def OM_PRECEDES(self, item1, item2):
        """
        Returns True if item1 appears before item2 in the order.
        Raises an exception if either item is not found.
        """
        try:
            idx1 = self.order.index(item1)
            idx2 = self.order.index(item2)
        except ValueError as e:
            raise ValueError("OM_PRECEDES Error: One or both items not found in the order.") from e
        return idx1 < idx2

    def display_order(self):
        """
        Returns a copy for the current order for external inspection.
        """
        return self.order.copy()
    
# Example usage:
if __name__ == "__main__":
    # Create an instance of the order-maintenance data structure.
    om_eng = OrderMaintenance()
    om_hebrew = OrderMaintenance()
    
    # For demonstration, we use simple string identifiers.
    # In a full prototype, these could be thread objects or unique thread IDs.
    
    # Initialize the orders with a first thread.
    om_eng.OM_INSERT("Thread-1")
    om_hebrew.OM_INSERT("Thread-1")
    
    # Insert additional threads. For an S-node insertion,
    # we insert the left child and then the right child in both orders.
    om_eng.OM_INSERT("Thread-2", after_item="Thread-1")
    om_hebrew.OM_INSERT("Thread-2", after_item="Thread-1")
    
    om_eng.OM_INSERT("Thread-3", after_item="Thread-2")
    om_hebrew.OM_INSERT("Thread-3", after_item="Thread-2")
    
    # Example: for a P-node, suppose the English order inserts children left-to-right
    # while the Hebrew order inserts them right-to-left.
    #
    # Insert two threads representing the children of a P-node.
    om_eng.OM_INSERT("Thread-4", after_item="Thread-3")
    # In the Hebrew order, we simulate reverse insertion:
    om_hebrew.OM_INSERT("Thread-5", after_item="Thread-1")  # Imagine this as the first insertion
    om_hebrew.OM_INSERT("Thread-4", after_item="Thread-5")
    
    # Display the maintained orders.
    print("English Order:", om_eng.display_order())
    print("Hebrew Order:", om_hebrew.display_order())
    
    # Reachability queries using OM_PRECEDES.
    # For example, if in both orders "Thread-1" precedes "Thread-3", then
    # by the SP-maintenance property, Thread-1 precedes Thread-3.
    eng_precedes = om_eng.OM_PRECEDES("Thread-1", "Thread-3")
    hebrew_precedes = om_hebrew.OM_PRECEDES("Thread-1", "Thread-3")
    print("Does 'Thread-1' precede 'Thread-3' in English order?", eng_precedes)
    print("Does 'Thread-1' precede 'Thread-3' in Hebrew order?", hebrew_precedes)
    
    # Combined SP_PRECEDES: Thread-1 is considered to precede Thread-3
    # if and only if it precedes it in both orders.
    sp_precedes = eng_precedes and hebrew_precedes
    print("According to SP-maintenance, does 'Thread-1' precede 'Thread-3'?", sp_precedes)
