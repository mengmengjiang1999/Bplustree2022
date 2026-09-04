"""Node types for a B+ tree with fan-out three."""


class KeySet:
    NUM_KEYS = 2

    def __init__(self, keys=None):
        self.keys = list(keys) if keys is not None else [None] * self.NUM_KEYS

    def __str__(self):
        return str(self.keys)

    __repr__ = __str__

    def __hash__(self):
        return hash(tuple(self.keys))

    def __eq__(self, other):
        return isinstance(other, KeySet) and self.keys == other.keys


class PointerSet:
    FAN_OUT = 3

    def __init__(self, pointers=None):
        self.pointers = list(pointers) if pointers is not None else [None] * self.FAN_OUT

    def __str__(self):
        return str(self.pointers)

    __repr__ = __str__

    def __hash__(self):
        return hash(tuple(self.pointers))

    def __eq__(self, other):
        return isinstance(other, PointerSet) and self.pointers == other.pointers


class Node:
    def __init__(self, keys=None, pointers=None):
        self.keys = keys if keys is not None else KeySet()
        self.pointers = pointers if pointers is not None else PointerSet()

    def __str__(self):
        return "Node({}|{})".format(self.keys, self.pointers)

    __repr__ = __str__

    def __hash__(self):
        return hash((self.keys, self.pointers))

    def __eq__(self, other):
        return (
            isinstance(other, Node)
            and self.keys == other.keys
            and self.pointers == other.pointers
        )

    @staticmethod
    def get_num_keys():
        return KeySet.NUM_KEYS

    @staticmethod
    def get_fan_out():
        return PointerSet.FAN_OUT
