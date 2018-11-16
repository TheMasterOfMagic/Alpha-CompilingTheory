from functools import partial
from exp2.reachable_graph import ReachableGraph


class Production:
  def __init__(self, left_part: str, right_part: str):
    left_part, right_part = str(left_part), str(right_part)
    self.left_part, self.right_part = left_part, right_part

  def __str__(self):
    return '{:<2}→ {}'.format(self.left_part, self.right_part)

  def __iter__(self):
    yield self.left_part
    yield self.right_part

  def __lt__(self, other):
    assert isinstance(other, Production)
    _ = (a_left, b_left) = self.left_part, other.left_part
    a_prime, b_prime = a_left.endswith('\''), b_left.endswith('\'')
    # 如果只有一边以撇结尾
    if a_prime ^ b_prime:
      rv = a_prime and not b_prime
    # 如果两边都或都不以撇结尾
    else:
      a_s, b_s = a_left[0] == 'S', b_left[0] == 'S'
      # 如果只有一边首字符是S
      if a_s ^ b_s:
        rv = a_s and not b_s
      # 如果两边首字符都是S
      else:
        rv = a_left < b_left if a_left != b_left else self.right_part < other.right_part
    return rv


class Project:
  def __init__(self, production: Production or tuple, dot_index: int=0):
    production = Production(*production)
    dot_index = int(dot_index)
    assert dot_index <= len(production.right_part)
    self.production, self.dot_index = production, dot_index

    # 记录该项目能否继续向前移动
    self.able_to_step = dot_index < len(production.right_part)

    # 生成内部成员变量
    (left_part, right_part), index = self.production, self.dot_index
    self._str = str(Production(left_part, right_part[:index] + '·' + right_part[index:]))
    self.next = (self.production.right_part[self.dot_index:self.dot_index+1] or [''])[0]

  def step(self):
    assert self.able_to_step
    return Project(self.production, self.dot_index + 1)

  def __str__(self):
    return self._str

  def __lt__(self, other):
    assert isinstance(other, Project)
    return self.production < other.production \
      if self.production != other.production \
      else self.dot_index < other.dot_index


class State:
  def __init__(self, core_projects: set):
    core_projects = set(core_projects)
    assert all(isinstance(project, Project) for project in core_projects)
    self.projects = core_projects

  @property
  def nexts(self):
    """返回当前项目集可以消耗的字符的集合"""
    return set(filter(bool, (project.next for project in self.projects)))

  def step(self):
    return State(set(project.step() for project in self.projects if project.able_to_step))

  def __str__(self):
    return '\n'.join(map(str, sorted(self.projects)))
  # def build(self, productions: dict):
  #   """根据核心项目集构建完整项目集"""
  #   productions = dict((k, set(v)) for k, v in productions.items())
  #   dependencies_table = dict((k, set(v[0] for v in v_set if v[0].isupper())) for k, v_set in productions.items())
  #   dependencies_graph = Graph(dependencies_table)
  #   for c in ['S\''] + list('SAB'):
  #     print(dependencies_graph.get_reachable(c))


class PrefixDFA:
  pass


def main():
  productions = {
    'S\'': {'S'},
    'S': {'Aa', 'Bb'},
    'A': {'a', 'aa'},
    'B': {'b', 'bb'}
  }
  productions = set(Production(k, v) for k, v_set in productions.items() for v in v_set)
  projects = set(map(Project, productions))
  state = State(projects)
  print(state)


if __name__ == '__main__':
  main()
