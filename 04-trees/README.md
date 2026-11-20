# 04 - Trees

Binary search tree and balanced variants. Guiding questions: why does a BST degenerate to O(n)? How do AVL and Red-Black trees guarantee O(log n) height?

- [x] Binary search tree: insertion (iterative and recursive)
- [x] Binary search tree: search (iterative and recursive)
- [x] Binary search tree: deletion (leaf, one child, two children)
- [x] Traversals (in-order, pre-order, post-order, level-order), plus iterative pre-order and level-order grouped by level
- [x] Height (depth-first and breadth-first)
- [x] Interview problems: invert the tree, validate a BST, lowest common ancestor
- [ ] AVL (rotations)
- [ ] Red-Black

## Binary tree and BST

Implementation: [tree.py](tree.py). Each node holds a value and two pointers, `left` and `right`. The tree keeps a pointer to the `root`.

Whether it is a BST depends on how it is used. `insert` keeps the BST rule, and `search`, `delete` and `lowest_common_ancestor` rely on it. The rule applies to whole subtrees, not only to direct children: everything in a node's left subtree is smaller than it, and everything in the right subtree is larger. Duplicates are ignored, so the tree behaves like a set. `invert` mirrors the tree and breaks the rule; after it, the tree is only a binary tree.

## Complexity

Below, `n` is the number of nodes, `h` the height and `w` the width of the widest level. In a balanced tree `h` is about log2(n); in the worst case `h` is `n`.

| Operation | Time | Space | Why |
|-----------|------|-------|-----|
| `insert(value)` | O(h) | O(1) | Walks down one path, going left or right at each node, until it finds an empty spot. |
| `insert_recursive(value)` | O(h) | O(h) | Same path, but each step is a call that stays on the stack until the insertion ends. |
| `search(value)` | O(h) | O(1) | Each comparison discards one side, like binary search. |
| `search_recursive(value)` | O(h) | O(h) | Same path, with one call per level on the stack. |
| `delete(value)` | O(h) | O(h) | One descent to the node and, with two children, one more to the in-order successor. |
| `pre_order()`, `in_order()`, `post_order()` | O(n) | O(h) | Visit each node once; the recursion stack is as deep as the tree is tall. |
| `pre_order_iterative()` | O(n) | O(h) | Same visits, with an explicit stack instead of the call stack. |
| `level_order()`, `level_order_grouped()` | O(n) | O(w) | Each node enters and leaves the queue once; the queue holds at most one level. |
| `height_dfs()` | O(n) | O(h) | Needs every node, because the longest path can be anywhere. |
| `height_bfs()` | O(n) | O(w) | Counts the levels; the queue holds one level at a time. |
| `invert()` | O(n) | O(h) | Swaps the children of every node once. |
| `is_bst()` | O(n) | O(h) | Checks every node against a range; can stop early at the first invalid node. |
| `lowest_common_ancestor(a, b)` | O(h) | O(1) | Walks down one path until the two values split. |

The space column does not count the returned list.

## Why a BST degenerates

Each `insert` costs O(h), and the tree has no mechanism to keep `h` small. Inserting values in ascending order (`1, 2, 3, 4, 5`) always goes right, so every node has only a right child. The tree becomes a linked list, `h` becomes `n`, and the O(h) operations become O(n). Balanced variants (AVL, Red-Black) exist to prevent exactly this.

## Recursive or iterative

Both versions cost the same time. The recursive one keeps one call per level on the stack, so it uses O(h) memory, and on a degenerate tree with about 1000 nodes or more it hits Python's recursion limit (`RecursionError`). The iterative versions do not have that limit.

## Depth-first and breadth-first

All traversals visit every node. They differ in which node comes next:

- **Depth-first** (pre, in, post-order) goes down one branch before coming back. The recursive versions share one helper; only the moment of the visit changes (before the left child, between the children, or after the right child), selected by the `Order` enum. The iterative pre-order uses a list as a stack and pushes the right child before the left one, so the left comes out first.
- **Breadth-first** (`level_order`) uses a queue (`deque`), because the first node to enter must be the first to leave: the children of a level wait behind all the nodes of that level. To group by level (`level_order_grouped`, `height_bfs`), save the queue size at the start of each level and take exactly that many nodes.

## Deletion

- **Leaf**: the parent's pointer becomes `None`.
- **One child**: the child takes the place of the removed node.
- **Two children**: the node stays, and its value is replaced by the in-order successor (the smallest value in the right subtree). The successor is then deleted from the right subtree. It never has a left child, so that second deletion is always one of the two simple cases.

## Validating a BST

Comparing each node only with its direct children is not enough: a value can be correct for its parent and still be on the wrong side of an older ancestor. `is_bst` passes a range down the tree. Going left narrows the maximum to the current value; going right narrows the minimum. Every node must fit the range inherited from all its ancestors.

## Edge cases handled

Empty tree, single node, duplicate values (ignored), ascending insertion (degenerate tree), deleting a missing value, and invalid trees built by hand for `is_bst`.

## Files

- [tree.py](tree.py): `Node`, `Tree`, the `Order` enum, and the `test_*` functions with `assert`. Running the file executes all of them and prints `ok:` for each one that passes.
