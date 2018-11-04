from PriorTable import PriorTable
from collections import OrderedDict
import re


def calc_prior_table(g):
  g['S'] = ['#{}#'.format(list(g.keys())[0])]
  # 计算关系图
  first_graph = dict()
  last_graph = dict()
  for left_part, right_part_list in g.items():
    first_graph[left_part] = set()
    last_graph[left_part] = set()
    for right_part in right_part_list:
      vt_list = list(filter(lambda _: not _.isupper(), right_part))
      first_graph[left_part].add(right_part[0])
      last_graph[left_part].add(right_part[-1])
      if vt_list:
        first_graph[left_part].add(vt_list[0])
        last_graph[left_part].add(vt_list[-1])
      first_graph[left_part].difference_update({left_part})
      last_graph[left_part].difference_update({left_part})
  # 计算FirstVT集
  first_vt = dict()
  while first_graph:
    for k, v_set in first_graph.copy().items():
      # 如果所有指向的非终结符的FirstVT集都已求得
      vn_list = list(filter(str.isupper, v_set))
      if all(map(lambda _: _ in first_vt, vn_list)):
        first_vt[k] = set()
        for c in v_set:
          first_vt[k].update(first_vt[c]) if c.isupper() else first_vt[k].add(c)
        first_graph.pop(k)
  # 计算LastVT集
  last_vt = dict()
  while last_graph:
    for k, v_set in last_graph.copy().items():
      # 如果所有指向的非终结符的LastVT集都已求得
      vn_list = list(filter(str.isupper, v_set))
      if all(map(lambda _: _ in last_vt, vn_list)):
        last_vt[k] = set()
        for c in v_set:
          last_vt[k].update(last_vt[c]) if c.isupper() else last_vt[k].add(c)
        last_graph.pop(k)
  # 生成优先关系表
  rv = PriorTable()
  for left_part, right_part_list in g.items():
    for right_part in right_part_list:
      # 求'<'与'>'关系
      for a, b in zip(right_part[:-1], right_part[1:]):
        if not a.isupper() and b.isupper():
          for c in first_vt[b]:
            if rv[a, c] and rv[a, c] != -1:
              raise Exception
            rv[a, c] = -1
        elif a.isupper() and not b.isupper():
          for c in last_vt[a]:
            if rv[c, b] and rv[c, b] != 1:
              raise Exception
            rv[c, b] = 1
        else:
          raise Exception
      # 求'='关系
      vt_list = list(filter(lambda _: not _.isupper(), right_part))
      for a, b in zip(vt_list[:-1], vt_list[1:]):
        if rv[a, b] and rv[a, b] != 0:
          raise Exception
        rv[a, b] = 0
  return rv


def reduce(g: dict, expression: str):
  g_ = dict((re.sub(r'[A-Z]+', 'F', value), re.sub(r'[A-Z]+', 'F', key))
            for key, value_list in grammar.items() for value in value_list)
  pt = calc_prior_table(g)
  num_stk = ['#']
  sym_stk = ['#']
  num_exp = list(expression + '#')
  sym_exp = list(re.sub(r'\d+', 'i', expression) + '#')
  while sym_stk and sym_exp:
    print()
    num = num_exp[0]
    sym = sym_exp[0]
    top = list(e for e in sym_stk[::-1] if e in pt.keys())[0]
    print('{} ←→ {}'.format(''.join(sym_stk), ''.join(sym_exp)))
    print('{} ←→ {}'.format(''.join(num_stk), ''.join(num_exp)))
    print('关系: {} {} {}'.format(
      top,
      {-1: '<', 0: '=', 1: '>'}.get(pt[top, sym], '?'),
      sym
    ))
    if pt[top, sym] is None:
      print('不接受')
      break
    elif pt[top, sym] != 1:  # 移进
      if top == sym == '#':
        print('接受')
        break
      print('移进')
      sym_stk.append(sym)
      num_stk.append(num)
      sym_exp.pop(0)
      num_exp.pop(0)
    else:  # 归约
      print('归约')
      i, j = -2, -1
      while sym_stk[i] not in pt.keys() or sym_stk[j] not in pt.keys() or pt[sym_stk[i], sym_stk[j]] == 0:
        i -= 1
        if sym_stk[i] in pt.keys():
          j -= 1
      sym_right_part = ''.join(sym_stk[i + 1:])
      num_right_part = ''.join(num_stk[i + 1:])
      print('句柄: {}'.format(sym_right_part))
      if sym_right_part not in g_:
        print('无法归约, 因为没有以{}为右部的产生式'.format(sym_right_part))
        break
      sym_left_part = g_[sym_right_part]
      num_left_part = str(eval(num_right_part.replace('^', '**')))
      print('{} → {}'.format(sym_left_part, sym_right_part))
      print('{} → {}'.format(num_left_part, num_right_part))
      sym_stk[i + 1:] = [sym_left_part]
      num_stk[i + 1:] = [num_left_part]


if __name__ == '__main__':
  grammar = OrderedDict(
    E=['E+T', 'E-T', 'T'],
    T=['T*F', 'T/F', 'F'],
    F=['P^F', 'P'],
    P=['(E)', 'i']
  )

  # grammar = dict(
  #   F=['F+F', 'F*F', 'F^F', '(F)', 'i']
  # )

  reduce(grammar, '((1+4)*3)^(2*(6-5))')
