from collections import OrderedDict
from pprint import pprint


class PriorTable:
  def __init__(self):
    self.table = OrderedDict()
    self.items = self.table.items
    self.keys = self.table.keys

  def __getitem__(self, item):
    a, *b = item
    if not b:
      self.table.setdefault(a, OrderedDict())
      return self.table[a]
    [b] = b
    if a not in self.table:
      self.table.setdefault(a, OrderedDict())
    return self.table[a].get(b, None)

  def __setitem__(self, key, value):
    a, b = key
    if a not in self.table:
      self.table.setdefault(a, OrderedDict())
    self.table[a][b] = value

  def show(self):
    """
    以稍微比较美观的方式打印一个二维字典
    """
    pprint(self.table)
