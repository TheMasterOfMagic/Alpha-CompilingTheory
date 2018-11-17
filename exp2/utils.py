t_count = 0
line_feed = True
DEBUG = False


def debug(_debug):
  def outer_wrapper(func):
    def wrapper(*args, **kwargs):
      global DEBUG
      switched = False
      if _debug != DEBUG:
        DEBUG = _debug
        switched = True
      tmp = t_count
      rv = func(*args, **kwargs)
      assert tmp == t_count
      if switched:
        DEBUG = not _debug
      return rv

    return wrapper

  return outer_wrapper


def log(*args, **kwargs):
  global t_count, line_feed, DEBUG
  if DEBUG:
    tc = kwargs.pop('tc', 0)
    end = kwargs.get('end', '\n')
    t_count += tc
    if line_feed:
      print('\t' * t_count, end='')
    print(*args, **kwargs)
    t_count -= tc

    line_feed = '\n' in end


prd_fmt = '{} → {}'


def log_up(tc=1):
  global t_count
  t_count += tc


def log_down(tc=1):
  global t_count
  t_count -= tc


epsl = 'ϵ'


def cacheable(cls):
  def new(cls_, *args, **kwargs):
    d: dict = {
      set: frozenset,
      list: tuple,
      dict: lambda _: frozenset(_.items())
    }
    args = tuple(d.get(type(arg), lambda _: _)(arg) for arg in args)
    key = hash((hash(args), hash(frozenset(kwargs.items()))))
    if key not in cls_.cache:
      instance = object.__new__(cls_)
      instance.__init__(*args, **kwargs)
      cls_.cache[key] = instance
    return cls_.cache[key]

  def repr_(self):
    return '<{} {}>'.format(cls.__name__, str(self))

  cls.cache = dict()
  cls.__new__ = new
  cls.__repr__ = repr_
  return cls


def analyze_reachable_graph(table: dict, key=None):
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
  return reachable_graph
