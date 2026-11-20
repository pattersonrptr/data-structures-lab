# 04 - Trees

Binary search tree and balanced variants. Guiding questions: why does a BST degenerate to O(n)? How do AVL and Red-Black trees guarantee O(log n) height?

- [x] Binary search tree: insertion
- [ ] Binary search tree: search
- [ ] Binary search tree: deletion
- [x] Traversals (in-order, pre-order, post-order, level-order)
- [ ] AVL (rotations)
- [ ] Red-Black

## Binary search tree

Implementation: [binary_search_tree.py](binary_search_tree.py). Each node holds a value and two pointers, `left` and `right`. The tree keeps a pointer to the `root`. The ordering rule applies to whole subtrees, not only to direct children: everything in a node's left subtree is smaller than it, and everything in the right subtree is larger. Duplicates are ignored, so the tree behaves like a set.

Below, `h` is the height of the tree and `n` the number of nodes. In a balanced tree `h` is about log2(n); in the worst case `h` is `n`.

| Operation | Time | Space | Why |
|-----------|------|-------|-----|
| `insert(value)` | O(h) | O(1) | Walks down one path, going left or right at each node, until it finds an empty spot. |
| `pre_order()` | O(n) | O(h) | Visits each node once; the recursion stack is as deep as the tree is tall. |
| `in_order()` | O(n) | O(h) | Same as above. On a BST it returns the values sorted. |
| `post_order()` | O(n) | O(h) | Same as above. |
| `level_order()` | O(n) | O(w) | Each node enters and leaves the queue once; the queue holds at most one level, and `w` is the widest level. |

The space column does not count the returned list, which always has `n` values.

## Why a BST degenerates

Each `insert` costs O(h), and the tree has no mechanism to keep `h` small. Inserting values in ascending order (`1, 2, 3, 4, 5`) always goes right, so every node has only a right child. The tree becomes a linked list, `h` becomes `n`, and the operations become O(n). Balanced variants (AVL, Red-Black) exist to prevent exactly this.

## Depth-first and breadth-first

All traversals visit every node. They differ in which node comes next:

- **Depth-first** (pre, in, post-order) goes down one branch before coming back. It is recursive, and the call stack is what remembers the nodes still to visit. The three orders share one helper; only the moment of the visit changes (before the left child, between the children, or after the right child), selected by the `Order` enum.
- **Breadth-first** (`level_order`) visits level by level. It uses a queue (`deque`), because the first node to enter must be the first to leave: the children of a level wait behind all the nodes of that level.

## Edge cases handled

Empty tree (all traversals return `[]`), single node, duplicate values (ignored), and ascending insertion (degenerate tree).

## Files

- [binary_search_tree.py](binary_search_tree.py): `Node`, `Tree`, the `Order` enum, and the `test_*` functions with `assert`. Running the file executes all of them and prints `ok:` for each one that passes.
