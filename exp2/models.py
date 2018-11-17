from exp2.utils import *


@cacheable
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

  def __repr__(self):
    return '<Production {} >'.format(str(self))


@cacheable
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
    return self.dot_index > other.dot_index \
      if self.dot_index != other.dot_index \
      else self.production < other.production

  def __iter__(self):
    yield self.production
    yield self.dot_index


@cacheable
class State:
  def __init__(self, core_projects: set, hard_step_dict=None, id_=None):
    core_projects = set(Project(*project) for project in core_projects)
    self.projects = core_projects
    self.hard_step_dict = hard_step_dict or dict()
    self.id = id_

  @property
  def nexts(self):
    """返回当前项目集中所有位于点号后面的字符的集合"""
    return sorted(set(filter(bool, (project.next for project in self.projects))))

  @property
  def next_vns(self):
    """返回当前项目集中所有位于点号后面的非终结符的集合"""
    return sorted(set(filter(str.isupper, self.nexts)))

  def step(self, character):
    return State(set(project.step() for project in self.projects if project.next == character))

  def set_hard_step(self, character: str, state):
    character, state = str(character), state
    self.hard_step_dict[character] = state

  def __str__(self):
    return ' | '.join(map(str, sorted(self.projects)))

  def __iter__(self):
    yield self.projects.copy()
    yield self.hard_step_dict.copy()
    yield self.id
