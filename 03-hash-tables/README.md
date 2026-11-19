# 03 - Hash tables

Average O(1) access via a hash function. Guiding questions: what happens with collisions (chaining vs. open addressing)? When does the table need to be resized?

- [x] Hash function
- [x] Chaining
- [ ] Open addressing (linear and double probing)
- [x] Resizing and load factor

Implementation: [hash_table.py](hash_table.py) (chaining, doubles the table when the load factor goes above 0.75). Running the file executes checks for basic operations, collisions, and resizing.
