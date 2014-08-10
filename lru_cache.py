from Queue import deque


class lru_cache:
  def __init__(self, capacity):
    self.queue = deque()
    self.capacity = capacity
    self.node_map = {}
    self.head = None

  def enqueue(self, key, value):
    new_node = Node(key, value)
    self.queue.appendleft(new_node)
    self.node_map[key] = new_node
    self.head = new_node

  def __getitem__(self, key):
    if key in self.node_map.keys():
      node = self.node_map[key]
      if node == self.head:
        return node.value
      self.enqueue(node.key, node.value)
      return node.value
    else:
      return None

  def __setitem__(self, key, value):
    if self[key] is None:
      self.enqueue(key, value)
      if len(self.node_map.keys()) > self.capacity:
        evicted = self.queue.pop()
        del self.node_map[evicted.key]
    else:
      self.head.value = value


class Node:
  def __init__(self, key, value):
    self.key = key
    self.value = value
