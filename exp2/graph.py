class Graph:
  def __init__(self, table: dict):
    table = dict((k, set(v)) for k, v in table.items())
    self.table = table
    self._cache_get_reachable = dict()

  def get_reachable(self, node) -> set:
    """获取从某个节点开始所能到达的所有节点"""
    if node not in self._cache_get_reachable:
      reachable = set()
      queue = [node]
      visited = set()
      while len(queue) > 0:
        current = queue.pop(0)
        if current not in visited:
          reachable.add(current)
          visited.add(current)
          nodes = self.table.get(current, set())
          list(map(queue.append, nodes))
      self._cache_get_reachable[node] = reachable
    rv = self._cache_get_reachable[node]
    return rv
