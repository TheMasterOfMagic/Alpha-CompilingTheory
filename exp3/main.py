from PriorTable import PriorTable
from collections import OrderedDict

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


def reduce(pt: PriorTable, s: str):
	stack = ['#']
	s = list(s + '#')
	while stack and s:
		print()
		c = s[0]
		top = list(e for e in stack[::-1] if e in pt.keys())[0]
		print('{} —— {}'.format(''.join(stack), ''.join(s)))
		if pt[top, c] != 1:  # 移进
			if top == c == '#':
				print('接受')
				break
			print('移进')
			stack.append(c)
			s.pop(0)
		else:  # 归约
			print('归约')
			i, j = -2, -1
			while stack[i] not in pt.keys() or stack[j] not in pt.keys() or prior_table[stack[i], stack[j]] == 0:
				i -= 1
				if stack[i] in pt.keys():
					j -= 1
			right_part = stack[i + 1:]
			left_part = g_[''.join(right_part)]
			print('{} → {}'.format(left_part, ''.join(right_part)))
			stack[i+1:] = [left_part]


reduce(prior_table, '((i+i)*i)*(i+i)')
