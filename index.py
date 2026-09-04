"""B+ tree index container."""

from node import Node


class Index:
    NUM_KEYS = Node.get_num_keys()
    FAN_OUT = Node.get_fan_out()

    def __init__(self, root=None):
        self.root = root if root is not None else Node()

    def __str__(self):
        return str(self.root)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.root)

    def __eq__(self, other):
        return isinstance(other, Index) and self.root == other.root
