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
    ]

    for test in tests:
        test()
        print("ok:", test.__name__)
