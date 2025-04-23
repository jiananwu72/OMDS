import networkx as nx
from SimpleSimulator import make_race_dag, make_no_race_dag
from OrderMaintenance import OrderMaintenance

class SPRaceDetector:
    def __init__(self, G, om_class):
        self.graph = G
        # two OM structures
        self.eng = om_class()
        self.heb = om_class()
        # maps from your parse-node IDs (str) to the OMNode objects
        self.eng_map = {}
        self.heb_map = {}

    def sp_order(self, X):
        # get children list (None on leaves)
        children = self.graph.nodes[X].get('children')
        if not children:
            return

        left, right = children

        # 1) If this is the very first insert of X, seed both OM's with it
        if self.graph.in_degree(X) == 0:
            eng_node = self.eng.insert_after(None, X)
            heb_node = self.heb.insert_after(None, X)
            self.eng_map[X] = eng_node
            self.heb_map[X] = heb_node

        # 2) English OM: insert left then right
        eng_node = self.eng_map[X]
        eng_left = self.eng.insert_after(eng_node, left)
        eng_right = self.eng.insert_after(eng_left, right)
        self.eng_map[left]  = eng_left
        self.eng_map[right] = eng_right

        # 3) Hebrew OM: order depends on S vs. P
        heb_node = self.heb_map[X]
        if X.startswith('S'):
            heb_left  = self.heb.insert_after(heb_node, left)
            heb_right = self.heb.insert_after(heb_left, right)
        else:
            heb_right = self.heb.insert_after(heb_node, right)
            heb_left  = self.heb.insert_after(heb_right, left)

        self.heb_map[left]  = heb_left
        self.heb_map[right] = heb_right

        # 4) recurse
        self.sp_order(left)
        self.sp_order(right)

    def sp_precedes(self, X, Y):
        # still pass the raw IDs here
        return (self.eng.comes_before(self.eng_map[X], self.eng_map[Y]) and
                self.heb.comes_before(self.heb_map[X], self.heb_map[Y]))


if __name__ == "__main__":
    race_dag    = make_race_dag()
    no_race_dag = make_no_race_dag()

    detector = SPRaceDetector(race_dag, OrderMaintenance)