from PriorTable import PriorTable
from collections import OrderedDict
import re

prior_table = PriorTable()

normal_operators = OrderedDict({
	'+': (1, -1),
	'-': (1, -1),
	'*': (2, -1),
	'/': (2, -1),
	'^': (3, 1)
})

# 设置各运算符的优先级
if 1:
	# 普通运算符
	for left in normal_operators.items():
		for right in normal_operators.items():
			left_op, (left_lv, left_dir) = left
			right_op, (right_lv, right_dir) = right
			if left_lv != right_lv:
				prior_table[left_op, right_op] = -1 if left_lv < right_lv else 1
			else:
				if left_dir == right_dir == -1:  # 左结合
					prior_table[left_op, right_op] = 1
				elif left_dir == right_dir == 1:  # 右结合
					prior_table[left_op, right_op] = -1
				else:
					raise Exception('WTF is GOING ON???')  # 给出醒目的异常提示
	# 特殊运算符
	for normal_op in normal_operators:
		prior_table['(', normal_op] = prior_table[normal_op, '('] = -1
		prior_table[')', normal_op] = prior_table[normal_op, ')'] = 1
	prior_table['(', '('] = -1
	prior_table['(', ')'] = 0
	prior_table[')', ')'] = 1
	# i运算符
	for op in list(normal_operators) + list('()'):
		if op != '(':
			prior_table['i', op] = 1
		if op != ')':
			prior_table[op, 'i'] = -1
	# 井号运算符
	for op in list(normal_operators) + list('()i'):
		prior_table['#', op] = -1
		prior_table[op, '#'] = 1
	prior_table['#', '#'] = 0

# g = dict(
# 	E=['E+T', 'T'],
# 	T=['T*F', 'F'],
# 	F=['P^F', 'P'],
# 	P=['(E)', 'i']
# )

g = dict(
	F=['F+F', 'F*F', 'F^F', '(F)', 'i']
)

g_ = dict((value, key) for key, value_list in g.items() for value in value_list)


def reduce(pt: PriorTable, expression: str):
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
		if pt[top, sym] != 1:  # 移进
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
			while sym_stk[i] not in pt.keys() or sym_stk[j] not in pt.keys() or prior_table[sym_stk[i], sym_stk[j]] == 0:
				i -= 1
				if sym_stk[i] in pt.keys():
					j -= 1
			sym_right_part = ''.join(sym_stk[i + 1:])
			num_right_part = ''.join(num_stk[i + 1:])
			sym_left_part = g_[sym_right_part]
			num_left_part = str(eval(num_right_part))
			print('{} → {}'.format(sym_left_part, sym_right_part))
			print('{} → {}'.format(num_left_part, num_right_part))
			sym_stk[i+1:] = [sym_left_part]
			num_stk[i+1:] = [num_left_part]


reduce(prior_table, '((1+2)*3)*(4+5)')
