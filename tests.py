import random
import unittest

from implement_me import ImplementMe
from index import Index
from node import KeySet, Node, PointerSet


def leaf(values, next_leaf=None):
    return Node(
        KeySet(values + [None] * (2 - len(values))),
        PointerSet([None, None, next_leaf]),
    )


class BPlusTreeTests(unittest.TestCase):
    def test_insert_into_empty_leaf_and_ignore_duplicate(self):
        tree = Index()
        self.assertIs(tree, ImplementMe.InsertIntoIndex(tree, 99))
        self.assertEqual([99, None], tree.root.keys.keys)
        ImplementMe.InsertIntoIndex(tree, 99)
        self.assertEqual([99, None], tree.root.keys.keys)

    def test_leaf_split(self):
        tree = Index(leaf([66, 99]))
        ImplementMe.InsertIntoIndex(tree, 87)

        left = tree.root.pointers.pointers[0]
        right = tree.root.pointers.pointers[1]
        self.assertEqual([87, None], tree.root.keys.keys)
        self.assertEqual([66, None], left.keys.keys)
        self.assertEqual([87, 99], right.keys.keys)
        self.assertIs(right, left.pointers.pointers[2])

    def test_lookup_checks_leaves_not_directory_separators(self):
        left = leaf([1])
        right = leaf([60])
        left.pointers.pointers[2] = right
        tree = Index(Node(KeySet([50, None]), PointerSet([left, right, None])))
        self.assertFalse(ImplementMe.LookupKeyInIndex(tree, 50))
        self.assertTrue(ImplementMe.LookupKeyInIndex(tree, 60))

    def test_range_search_is_half_open(self):
        tree = Index()
        for key in [99, 41, 87, 68]:
            ImplementMe.InsertIntoIndex(tree, key)
        self.assertEqual([41], ImplementMe.RangeSearchInIndex(tree, 0, 42))
        self.assertEqual([68, 87], ImplementMe.RangeSearchInIndex(tree, 42, 99))
        self.assertEqual([], ImplementMe.RangeSearchInIndex(tree, 7, 7))

    def test_splits_propagate_through_multiple_levels(self):
        keys = list(range(200))
        random.Random(370).shuffle(keys)
        tree = Index()
        for key in keys:
            ImplementMe.InsertIntoIndex(tree, key)

        self.assertEqual(list(range(200)), ImplementMe.RangeSearchInIndex(tree, 0, 200))
        for key in range(200):
            self.assertTrue(ImplementMe.LookupKeyInIndex(tree, key))
        self.assertFalse(ImplementMe.LookupKeyInIndex(tree, -1))
        self.assertFalse(ImplementMe.LookupKeyInIndex(tree, 200))
        self._assert_invariants(tree)

    def test_random_insert_lookup_and_ranges_match_python(self):
        for seed in range(20):
            randomizer = random.Random(seed)
            inserted = [randomizer.randrange(-100, 101) for _ in range(150)]
            expected = sorted(set(inserted))
            tree = Index()

            for key in inserted:
                ImplementMe.InsertIntoIndex(tree, key)

            self.assertEqual(expected, ImplementMe.RangeSearchInIndex(tree, -101, 102))
            for _ in range(20):
                lower = randomizer.randrange(-110, 111)
                upper = randomizer.randrange(-110, 111)
                wanted = [key for key in expected if lower <= key < upper]
                self.assertEqual(wanted, ImplementMe.RangeSearchInIndex(tree, lower, upper))
            for key in range(-110, 111):
                self.assertEqual(key in expected, ImplementMe.LookupKeyInIndex(tree, key))
            self._assert_invariants(tree)

    def _assert_invariants(self, tree):
        leaves = []
        leaf_depths = set()

        def visit(node, depth):
            keys = [key for key in node.keys.keys if key is not None]
            self.assertEqual(keys, sorted(keys))
            self.assertLessEqual(len(keys), 2)

            if node.pointers.pointers[0] is None:
                leaves.append(node)
                leaf_depths.add(depth)
                return keys

            children = node.pointers.pointers[: len(keys) + 1]
            self.assertTrue(all(child is not None for child in children))
            child_values = [visit(child, depth + 1) for child in children]
            for position, separator in enumerate(keys):
                self.assertEqual(separator, child_values[position + 1][0])
            return [key for values in child_values for key in values]

        values = visit(tree.root, 0)
        self.assertEqual(1, len(leaf_depths))
        self.assertEqual(values, sorted(values))
        for current, following in zip(leaves, leaves[1:]):
            self.assertIs(following, current.pointers.pointers[2])
        self.assertIsNone(leaves[-1].pointers.pointers[2])


if __name__ == "__main__":
    unittest.main(verbosity=2)
