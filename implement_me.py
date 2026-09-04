"""Insertion and search operations for the B+ tree index."""

from bisect import bisect_right

from index import Index
from node import KeySet, Node, PointerSet


def _keys(node):
    return [key for key in node.keys.keys if key is not None]


def _is_leaf(node):
    # Leaf nodes reserve the third pointer for the next leaf in key order.
    return node.pointers.pointers[0] is None


def _find_leaf(root, key):
    node = root
    while not _is_leaf(node):
        child_index = bisect_right(_keys(node), key)
        node = node.pointers.pointers[child_index]
    return node


def _insert(node, key):
    """Insert key below node and return (promoted_key, right_node) on split."""
    if _is_leaf(node):
        values = _keys(node)
        values.insert(bisect_right(values, key), key)

        if len(values) <= Node.get_num_keys():
            node.keys.keys = values + [None] * (Node.get_num_keys() - len(values))
            return None

        split_at = len(values) // 2
        left_values = values[:split_at]
        right_values = values[split_at:]
        old_next = node.pointers.pointers[2]
        right = Node(
            KeySet(right_values),
            PointerSet([None, None, old_next]),
        )
        node.keys.keys = left_values + [None] * (Node.get_num_keys() - len(left_values))
        node.pointers.pointers = [None, None, right]
        return right_values[0], right

    separators = _keys(node)
    children = node.pointers.pointers[: len(separators) + 1]
    child_index = bisect_right(separators, key)
    split = _insert(children[child_index], key)

    if split is None:
        return None

    promoted, right_child = split
    separators.insert(child_index, promoted)
    children.insert(child_index + 1, right_child)

    if len(separators) <= Node.get_num_keys():
        node.keys.keys = separators + [None] * (Node.get_num_keys() - len(separators))
        node.pointers.pointers = children + [None] * (Node.get_fan_out() - len(children))
        return None

    middle = len(separators) // 2
    promoted = separators[middle]
    left_keys = separators[:middle]
    right_keys = separators[middle + 1 :]
    left_children = children[: middle + 1]
    right_children = children[middle + 1 :]

    node.keys.keys = left_keys + [None] * (Node.get_num_keys() - len(left_keys))
    node.pointers.pointers = left_children + [None] * (Node.get_fan_out() - len(left_children))
    right = Node(
        KeySet(right_keys + [None] * (Node.get_num_keys() - len(right_keys))),
        PointerSet(right_children + [None] * (Node.get_fan_out() - len(right_children))),
    )
    return promoted, right


class ImplementMe:
    """Operations supported by the integer-key B+ tree."""

    @staticmethod
    def InsertIntoIndex(index, key):
        """Insert key if absent and return the index."""
        if ImplementMe.LookupKeyInIndex(index, key):
            return index

        split = _insert(index.root, key)
        if split is not None:
            promoted, right = split
            index.root = Node(
                KeySet([promoted, None]),
                PointerSet([index.root, right, None]),
            )
        return index

    @staticmethod
    def LookupKeyInIndex(index, key):
        """Return whether key occurs in a leaf node."""
        leaf = _find_leaf(index.root, key)
        return key in _keys(leaf)

    @staticmethod
    def RangeSearchInIndex(index, lower_bound, upper_bound):
        """Return sorted keys in the half-open interval [lower, upper)."""
        if lower_bound >= upper_bound:
            return []

        result = []
        leaf = _find_leaf(index.root, lower_bound)
        while leaf is not None:
            for key in _keys(leaf):
                if key >= upper_bound:
                    return result
                if key >= lower_bound:
                    result.append(key)
            leaf = leaf.pointers.pointers[2]
        return result
