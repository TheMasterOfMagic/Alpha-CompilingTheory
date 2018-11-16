

class ReachableGraph:
  def __init__(self, table: dict, key=None):
    table = dict((k, set(v)) for k, v in table.items())
    assert callable(key) or key is None

    reachable_graph = dict()
    for k in table:
      reachable = set()
      queue = [k]
      visited = set()
      while len(queue) > 0:
        current = queue.pop(0)
        if current not in visited:
          reachable.add(current)
          visited.add(current)
          nodes = table.get(current, set())
          list(map(queue.append, nodes))
      if key:
        reachable = set(filter(key, reachable))

      reachable_graph[k] = reachable

    self._reachable_graph = reachable_graph
    self.keys = reachable_graph.keys
    self.values = reachable_graph.values
    self.items = reachable_graph.items
    self.__iter__ = reachable_graph.__iter__

  def __getitem__(self, item):
    return self._reachable_graph[item]
