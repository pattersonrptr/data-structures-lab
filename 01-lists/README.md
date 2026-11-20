# 01 - Lists

Dynamic array and linked list. Guiding questions: why is index access O(1) in an array but O(n) in a list? Why is appending to the end of a dynamic array O(1) amortized?

- [ ] Dynamic array (resizing and growth factor)
- [x] Singly linked list
- [ ] Doubly linked list

## Singly linked list

Implementation: [linked_list.py](linked_list.py). Each node holds a value and a pointer to the next node. The list keeps pointers to both the first and the last node, plus a size counter.

| Operation | Time | Why |
|-----------|------|-----|
| `get(index)` | O(n) | There is no direct access: it walks from the first node, one `next` at a time. |
| `prepend(value)` | O(1) | Only rewires the `first` pointer. |
| `append(value)` | O(1) | The `last` pointer avoids walking the whole list. |
| `insert(value, index)` | O(n) | Walks to the node before `index`, then rewires two pointers (O(1) at the ends). |
| `contains(value)` | O(n) | Worst case checks every node. |
| `remove(value)` | O(n) | Walks to find the value, keeping the previous node so it can be unlinked. |
| `len(list)` | O(1) | Reads the counter instead of counting nodes. |
| iteration / `to_list()` | O(n) | Visits each node once. |

Edge cases handled: invalid index (`ValueError`), insert into an empty list, remove of the first and of the last node (updating `first` and `last`), and remove of a missing value (`ValueError`).

Running the file executes a small walkthrough of these operations.
