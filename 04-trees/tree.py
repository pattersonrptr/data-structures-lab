"""Binary tree.

Whether it is a binary search tree (BST) depends on how it is used.
`insert` keeps the BST ordering (smaller values to the left, larger to the
right), and `search` relies on that ordering. Operations such as `invert`
rearrange the nodes and break it; after them, the tree is only a binary tree.
"""

from enum import Enum
from collections import deque


class Order(Enum):
    PRE = "pre"
    IN = "in"
    POST = "post"


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class Tree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
            return

        current = self.root

        while current is not None:
            if value < current.value:
                if current.left is None:
                    current.left = Node(value)
                    break
                current = current.left
            elif value > current.value:
                if current.right is None:
                    current.right = Node(value)
                    break
                current = current.right
            else:
                break

    def pre_order(self):
        return self._depth_first(Order.PRE)

    def in_order(self):
        return self._depth_first(Order.IN)

    def post_order(self):
        return self._depth_first(Order.POST)

    def pre_order_iterative(self):
        result = []

        if self.root is None:
            return result

        stack = [self.root]

        while stack:
            node = stack.pop()
            result.append(node.value)

            # Right goes in first so that left comes out first.
            if node.right is not None:
                stack.append(node.right)

            if node.left is not None:
                stack.append(node.left)

        return result

    def _depth_first(self, order):
        result = []
        self._visit(self.root, order, result)
        return result

    def _visit(self, node, order, result):
        if node is None:
            return

        if order == Order.PRE:
            result.append(node.value)

        self._visit(node.left, order, result)

        if order == Order.IN:
            result.append(node.value)

        self._visit(node.right, order, result)

        if order == Order.POST:
            result.append(node.value)

    def level_order(self):
        result = []

        if self.root is None:
            return result

        queue = deque()
        queue.append(self.root)

        while queue:
            node = queue.popleft()
            result.append(node.value)

            if node.left is not None:
                queue.append(node.left)

            if node.right is not None:
                queue.append(node.right)

        return result

    def level_order_grouped(self):
        result = []

        if self.root is None:
            return result

        queue = deque([self.root])

        while queue:
            # The queue holds exactly one level here; process only those nodes.
            level_size = len(queue)
            level = []

            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.value)

                if node.left is not None:
                    queue.append(node.left)

                if node.right is not None:
                    queue.append(node.right)

            result.append(level)

        return result

    def search(self, value):
        current = self.root

        while current is not None:
            if value == current.value:
                return True
            elif value < current.value:
                current = current.left
            else:
                current = current.right

        return False

    def insert_recursive(self, value):
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if node is None:
            return Node(value)

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)

        return node

    def search_recursive(self, value):
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        if node is None:
            return False

        if value == node.value:
            return True

        if value < node.value:
            return self._search_recursive(node.left, value)

        return self._search_recursive(node.right, value)

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        # Returns the node that must take this place after the deletion.
        if node is None:
            return None

        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            # No child or one child: the child (or None) takes this node's place.
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # Two children: copy the in-order successor (smallest value on the
            # right), then delete the successor, which has no left child.
            successor = node.right
            while successor.left is not None:
                successor = successor.left

            node.value = successor.value
            node.right = self._delete(node.right, successor.value)

        return node

    def height_dfs(self):
        return self._height_dfs(self.root)

    def _height_dfs(self, node):
        if node is None:
            return 0

        return max(self._height_dfs(node.left), self._height_dfs(node.right)) + 1

    def height_bfs(self):
        if self.root is None:
            return 0

        queue = deque([self.root])
        height = 0

        while queue:
            # The queue holds exactly one level here; process only those nodes.
            level_size = len(queue)

            for _ in range(level_size):
                node = queue.popleft()

                if node.left is not None:
                    queue.append(node.left)

                if node.right is not None:
                    queue.append(node.right)

            height += 1

        return height

    def invert(self):
        # Mirrors the tree in place. Afterwards it is no longer a BST,
        # so insert and search stop working correctly.
        self._invert(self.root)

    def _invert(self, node):
        if node is None:
            return

        node.left, node.right = node.right, node.left

        self._invert(node.left)
        self._invert(node.right)

    def lowest_common_ancestor(self, a, b):
        # Assumes both values are in the tree.
        current = self.root

        while current is not None:
            if a < current.value and b < current.value:
                current = current.left
            elif a > current.value and b > current.value:
                current = current.right
            else:
                return current.value

        return None

    def is_bst(self):
        return self._is_bst(self.root, float("-inf"), float("inf"))

    def _is_bst(self, node, low, high):
        # Every node must fit the range inherited from all of its ancestors,
        # not only from its parent.
        if node is None:
            return True

        if not low < node.value < high:
            return False

        return (self._is_bst(node.left, low, node.value)
                and self._is_bst(node.right, node.value, high))


def build(values):
    tree = Tree()
    for value in values:
        tree.insert(value)
    return tree


def test_insert_builds_expected_shape():
    tree = build([5, 3, 8, 1])

    assert tree.root.value == 5
    assert tree.root.left.value == 3
    assert tree.root.right.value == 8
    assert tree.root.left.left.value == 1
    assert tree.root.left.right is None


def test_insert_ignores_duplicates():
    tree = build([5, 3, 8, 1])
    tree.insert(5)
    tree.insert(1)

    assert tree.in_order() == [1, 3, 5, 8]


def test_insert_ascending_order_degenerates_into_a_line():
    tree = build([1, 2, 3, 4, 5])

    current = tree.root
    while current is not None:
        assert current.left is None
        current = current.right

    assert tree.in_order() == [1, 2, 3, 4, 5]


def test_traversals_on_small_tree():
    tree = build([5, 3, 8, 1])

    assert tree.pre_order() == [5, 3, 1, 8]
    assert tree.in_order() == [1, 3, 5, 8]
    assert tree.post_order() == [1, 3, 8, 5]


def test_traversals_on_balanced_tree():
    tree = build([50, 30, 70, 20, 40, 60, 80])

    assert tree.pre_order() == [50, 30, 20, 40, 70, 60, 80]
    assert tree.in_order() == [20, 30, 40, 50, 60, 70, 80]
    assert tree.post_order() == [20, 40, 30, 60, 80, 70, 50]


def test_traversals_on_degenerate_tree():
    tree = build([1, 2, 3, 4, 5])

    assert tree.pre_order() == [1, 2, 3, 4, 5]
    assert tree.in_order() == [1, 2, 3, 4, 5]
    assert tree.post_order() == [5, 4, 3, 2, 1]


def test_traversals_on_empty_tree():
    tree = Tree()

    assert tree.pre_order() == []
    assert tree.in_order() == []
    assert tree.post_order() == []


def test_traversals_on_single_node():
    tree = build([7])

    assert tree.pre_order() == [7]
    assert tree.in_order() == [7]
    assert tree.post_order() == [7]


def test_in_order_is_sorted_regardless_of_insertion_order():
    tree = build([8, 3, 10, 1, 6, 14, 4, 7, 13])

    assert tree.in_order() == [1, 3, 4, 6, 7, 8, 10, 13, 14]


def test_level_order_on_small_tree():
    tree = build([5, 3, 8, 1])

    assert tree.level_order() == [5, 3, 8, 1]


def test_level_order_on_balanced_tree():
    tree = build([50, 30, 70, 20, 40, 60, 80])

    assert tree.level_order() == [50, 30, 70, 20, 40, 60, 80]


def test_level_order_differs_from_pre_order():
    tree = build([8, 3, 10, 1, 6, 14, 4, 7, 13])

    assert tree.level_order() == [8, 3, 10, 1, 6, 14, 4, 7, 13]
    assert tree.pre_order() == [8, 3, 1, 6, 4, 7, 10, 14, 13]


def test_level_order_on_degenerate_tree():
    tree = build([1, 2, 3, 4, 5])

    assert tree.level_order() == [1, 2, 3, 4, 5]


def test_level_order_on_empty_tree():
    tree = Tree()

    assert tree.level_order() == []


def test_level_order_on_single_node():
    tree = build([7])

    assert tree.level_order() == [7]


def test_search_finds_existing_values():
    tree = build([5, 3, 8, 1])

    for value in [5, 3, 8, 1]:
        assert tree.search(value) is True


def test_search_does_not_find_missing_values():
    tree = build([5, 3, 8, 1])

    assert tree.search(0) is False  # smaller than every value
    assert tree.search(4) is False  # between existing values
    assert tree.search(7) is False  # between existing values
    assert tree.search(9) is False  # larger than every value


def test_search_on_balanced_tree():
    tree = build([50, 30, 70, 20, 40, 60, 80])

    for value in [50, 30, 70, 20, 40, 60, 80]:
        assert tree.search(value) is True
    assert tree.search(65) is False


def test_search_on_degenerate_tree():
    tree = build([1, 2, 3, 4, 5])

    assert tree.search(5) is True
    assert tree.search(6) is False


def test_search_on_empty_tree():
    tree = Tree()

    assert tree.search(1) is False


def test_search_on_single_node():
    tree = build([7])

    assert tree.search(7) is True
    assert tree.search(6) is False


def test_height():
    cases = [
        ([], 0),
        ([7], 1),
        ([5, 3, 8, 1], 3),
        ([50, 30, 70, 20, 40, 60, 80], 3),
        ([1, 2, 3, 4, 5], 5),
    ]

    for values, expected in cases:
        tree = build(values)
        assert tree.height_dfs() == expected
        assert tree.height_bfs() == expected


def build_recursive(values):
    tree = Tree()
    for value in values:
        tree.insert_recursive(value)
    return tree


def test_insert_recursive_matches_iterative():
    cases = [
        [],
        [7],
        [5, 3, 8, 1],
        [5, 3, 8, 1, 5, 3],  # duplicates are ignored
        [50, 30, 70, 20, 40, 60, 80],
        [1, 2, 3, 4, 5],
    ]

    for values in cases:
        assert build_recursive(values).pre_order() == build(values).pre_order()


def test_search_recursive_matches_iterative():
    cases = [
        ([], [1]),
        ([7], [7, 6]),
        ([5, 3, 8, 1], [5, 3, 8, 1, 0, 4, 7, 9]),
        ([1, 2, 3, 4, 5], [5, 6]),
    ]

    for values, targets in cases:
        tree = build(values)
        for target in targets:
            assert tree.search_recursive(target) is tree.search(target)


def test_pre_order_iterative_matches_recursive():
    cases = [
        [],
        [7],
        [5, 3, 8, 1],
        [50, 30, 70, 20, 40, 60, 80],
        [1, 2, 3, 4, 5],
    ]

    for values in cases:
        tree = build(values)
        assert tree.pre_order_iterative() == tree.pre_order()


def test_level_order_grouped():
    cases = [
        ([], []),
        ([7], [[7]]),
        ([5, 3, 8, 1], [[5], [3, 8], [1]]),
        ([50, 30, 70, 20, 40, 60, 80], [[50], [30, 70], [20, 40, 60, 80]]),
        ([1, 2, 3, 4, 5], [[1], [2], [3], [4], [5]]),
    ]

    for values, expected in cases:
        tree = build(values)
        assert tree.level_order_grouped() == expected
        assert len(tree.level_order_grouped()) == tree.height_bfs()


DELETE_VALUES = [50, 30, 70, 20, 40, 60, 80, 65]


def test_delete_leaf():
    tree = build(DELETE_VALUES)
    tree.delete(20)

    assert tree.level_order_grouped() == [[50], [30, 70], [40, 60, 80], [65]]


def test_delete_node_with_one_child():
    tree = build(DELETE_VALUES)
    tree.delete(60)

    # 65 takes the place of 60, as the left child of 70.
    assert tree.level_order_grouped() == [[50], [30, 70], [20, 40, 65, 80]]


def test_delete_node_with_two_children():
    tree = build(DELETE_VALUES)
    tree.delete(50)

    # The successor 60 moves to the root, and 65 takes the old place of 60.
    assert tree.level_order_grouped() == [[60], [30, 70], [20, 40, 65, 80]]


def test_delete_missing_value_changes_nothing():
    tree = build(DELETE_VALUES)
    before = tree.level_order_grouped()
    tree.delete(99)

    assert tree.level_order_grouped() == before


def test_delete_on_empty_tree():
    tree = Tree()
    tree.delete(1)

    assert tree.root is None


def test_delete_all_values_one_by_one():
    tree = build(DELETE_VALUES)
    remaining = sorted(DELETE_VALUES)

    for value in DELETE_VALUES:
        tree.delete(value)
        remaining.remove(value)

        assert tree.is_bst() is True
        assert tree.search(value) is False
        assert tree.in_order() == remaining

    assert tree.root is None


def test_lowest_common_ancestor():
    tree = build([50, 30, 70, 20, 40, 60, 80])
    cases = [
        (20, 40, 30),  # same side of the root, they split at 30
        (20, 60, 50),  # opposite sides of the root
        (30, 20, 30),  # one value is an ancestor of the other
        (60, 80, 70),
        (40, 40, 40),  # a value with itself
    ]

    for a, b, expected in cases:
        assert tree.lowest_common_ancestor(a, b) == expected
        assert tree.lowest_common_ancestor(b, a) == expected


def test_lowest_common_ancestor_on_empty_tree():
    assert Tree().lowest_common_ancestor(1, 2) is None


def test_is_bst_on_trees_built_with_insert():
    cases = [
        [],
        [7],
        [5, 3, 8, 1],
        [50, 30, 70, 20, 40, 60, 80],
        [1, 2, 3, 4, 5],
    ]

    for values in cases:
        assert build(values).is_bst() is True


def test_is_bst_catches_value_in_the_wrong_subtree():
    # 7 is larger than its parent 3, but it sits left of 5.
    tree = build([5, 3, 8])
    tree.root.left.right = Node(7)

    assert tree.is_bst() is False


def test_is_bst_catches_wrong_direct_child():
    tree = build([5, 3, 8])
    tree.root.left.right = Node(2)

    assert tree.is_bst() is False


def test_is_bst_catches_duplicate():
    tree = build([5, 3, 8])
    tree.root.right.left = Node(5)

    assert tree.is_bst() is False


def test_is_bst_after_invert():
    tree = build([5, 3, 8, 1])
    tree.invert()

    assert tree.is_bst() is False


def test_invert():
    tree = build([5, 3, 8, 1])
    tree.invert()

    assert tree.level_order() == [5, 8, 3, 1]
    assert tree.in_order() == [8, 5, 3, 1]
    assert tree.root.right.right.value == 1


def test_invert_twice_restores_the_tree():
    tree = build([50, 30, 70, 20, 40, 60, 80])
    tree.invert()
    tree.invert()

    assert tree.pre_order() == [50, 30, 20, 40, 70, 60, 80]


def test_invert_on_empty_tree():
    tree = Tree()
    tree.invert()

    assert tree.level_order() == []


if __name__ == "__main__":
    tests = [
        test_insert_builds_expected_shape,
        test_insert_ignores_duplicates,
        test_insert_ascending_order_degenerates_into_a_line,
        test_traversals_on_small_tree,
        test_traversals_on_balanced_tree,
        test_traversals_on_degenerate_tree,
        test_traversals_on_empty_tree,
        test_traversals_on_single_node,
        test_in_order_is_sorted_regardless_of_insertion_order,
        test_level_order_on_small_tree,
        test_level_order_on_balanced_tree,
        test_level_order_differs_from_pre_order,
        test_level_order_on_degenerate_tree,
        test_level_order_on_empty_tree,
        test_level_order_on_single_node,
        test_search_finds_existing_values,
        test_search_does_not_find_missing_values,
        test_search_on_balanced_tree,
        test_search_on_degenerate_tree,
        test_search_on_empty_tree,
        test_search_on_single_node,
        test_height,
        test_insert_recursive_matches_iterative,
        test_search_recursive_matches_iterative,
        test_pre_order_iterative_matches_recursive,
        test_level_order_grouped,
        test_delete_leaf,
        test_delete_node_with_one_child,
        test_delete_node_with_two_children,
        test_delete_missing_value_changes_nothing,
        test_delete_on_empty_tree,
        test_delete_all_values_one_by_one,
        test_lowest_common_ancestor,
        test_lowest_common_ancestor_on_empty_tree,
        test_is_bst_on_trees_built_with_insert,
        test_is_bst_catches_value_in_the_wrong_subtree,
        test_is_bst_catches_wrong_direct_child,
        test_is_bst_catches_duplicate,
        test_is_bst_after_invert,
        test_invert,
        test_invert_twice_restores_the_tree,
        test_invert_on_empty_tree,
    ]

    for test in tests:
        test()
        print("ok:", test.__name__)
