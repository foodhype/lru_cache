from Queue import deque

class lru_cache:
  def __init__(self, capacity):
    self.queue = deque()
    self.capacity = capacity
    self.node_map = {}
    self.head = None

  def enqueue(self, key, value):
    new_node = (key, value)
    self.queue.appendleft(new_node)
    self.node_map[key] = new_node
    self.head = new_node

  def get(self, key):
    if key in self.node_map.keys():
      node = self.node_map[key]
      if node == self.head:
        return node[1]
      self.enqueue(node[0], node[1])
      return node[1]
    else:
      return None

  def set(self, key, value):
    if self.get(key) is None:
      self.enqueue(key, value)
      if len(self.node_map.keys()) > self.capacity:
        evicted = self.queue.pop()
        del self.node_map[evicted[0]]
    else:
      self.head[1] = value
