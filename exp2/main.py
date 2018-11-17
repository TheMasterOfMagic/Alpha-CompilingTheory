from exp2.grammar import Grammar


def main():
  e4_3 = dict(
    S=['aA', 'd'],
    A=['bAS', '']
  )
  e4_4 = dict(
    S=['aAS', 'b'],
    A=['bA', '']
  )
  e4_5 = dict(
    S=['AB', 'bC'],
    A=['', 'b'],
    B=['', 'aD'],
    C=['AD', 'b'],
    D=['aS', 'c'],
  )
  h4_4 = dict(
    E=['TR'],
    R=['+E', ''],
    T=['FY'],
    Y=['T', ''],
    F=['PG'],
    G=['*G', ''],
    P=['(E)', 'a', 'b', '^']
  )
  m1 = {
    'S': {'Aa', 'Bb'},
    'A': {'a', 'aa'},
    'B': {'b', 'bb'}
  }
  g = Grammar(m1, 'S')
  g.analyze_x()
  g.analyze_firsts()
  g.analyze_follows()
  g.analyze_selects()
  g.analyze_vn_dependencies()
  i0 = g.build_lr0_prefix_dfa()

  queue = [i0]
  state_list = list()
  while queue:
    current = queue.pop(0)
    print(current.id)
    print(current)
    print('Map:', ', '.join('{} → {}'.format(k, v.id) for k, v in current.hard_step_dict.items()))
    print()
    if current not in state_list:
      state_list.append(current)
      for node in current.hard_step_dict.values():
        if node not in state_list:
          queue.append(node)


if __name__ == '__main__':
  main()
