from collections import OrderedDict
from copy import deepcopy
from ultis import *


class Grammar:
	def __init__(self, table: OrderedDict):
		# 取有序字典里第一个key作为起始状态
		start = tuple(table)[0]
		self.start, self.table = start, table
		self.x = None
		self.firsts = None
		self.follows = None

	def show(self):
		for k, v_list in self.table.items():
			for v in v_list:
				log(prd_fmt.format(k, v or epsl))

	def copy(self):
		return Grammar(deepcopy(self.table))

	@debug(0)
	def analyze_x(self):
		log('分析各非终结符能否推出空串')
		log('当前有以下产生式: ')
		tmp = self.copy()
		log_up()
		tmp.show()
		log('其中: ', tc=-1)
		# 若某Vn的某个产生式的右部为ϵ，那它肯定能推出空串
		x = dict((vn, None) for vn in tmp.table)
		for k, v_list in tmp.copy().table.items():
			if any(map(lambda _: _ == '', v_list)):
				log('{}有一条右部为{}的产生式，故其肯定能推出空串'.format(k, epsl))
				x[k] = True
				tmp.table.pop(k)
		log_down()
		# 若某Vn的所有产生式的右部都含有Vt，那它肯定无法推出空串
		log('判断剩下的非终结符是否不能推出空串')
		log_up()
		for k in (filter(lambda _: x[_] is None, x)):
			log('判断{}是否不能推出空串: '.format(k))
			log_up()
			for v in tmp.table[k].copy():
				log(prd_fmt.format(k, v or epsl), end='')
				if not all(map(str.isupper, v)):
					log(' \t(含终结符，删除)')
					tmp.table[k].remove(v)
				else:
					log()
			if not tmp.table[k]:
				log('{}的所有产生式的右部均含有终结符，所以其肯定无法推出空串'.format(k))
				x[k] = False
				tmp.table.pop(k)
			log_down()
		log_down()
		log('判断完毕')
		# 开始循环扫描
		log('当前剩余的产生式:')
		log_up()
		tmp.show()
		log('开始循环扫描', tc=-1)
		while tmp.table:
			for k, v_list in tmp.table.copy().items():
				for v in v_list:
					log(('' + prd_fmt).format(k, v or epsl))
					log_up()
					for c in v + epsl:
						if c == epsl:
							log('已到达产生式右部的尾部')
							log('显然{}可以推出空串'.format(k), tc=1)
							x[k] = True
							tmp.table.pop(k)
							break
						log('{}'.format(c), end='')
						log(' {}推出空串'.format({True: '可以', False: '不能'}[x[c]]))
						if x[c] is True:
							log('所以需要看下一个符号', tc=1)
						elif x[c] is False:
							log('显然{}不能推出空串'.format(k), tc=1)
							x[k] = False
							tmp.table.pop(k)
							break
					log_down()
		log_down()
		self.x = x

	@debug(1)
	def analyze_firsts(self):
		self.show()
		log('开始扫描各产生式以构造First集关系图')
		first_relation = dict()
		log_up()
		for k, v_list in self.table.items():
			for v in v_list:
				log('当前产生式: ' + prd_fmt.format(k, v or epsl))
				log_up()
				for c in v:
					log('当前字符: {}'.format(c))
					first_relation.setdefault(k, set())
					first_relation[k].add(c)
					log_up()
					if c.islower() or not self.x[c]:
						log('其不能推出空串')
						log('故当前产生式已分析完毕')
						log_down()
						break
					else:
						log('其能推出空串')
						log('故仍需判断下一字符')
					log_down()
				else:
					log('已到达当前产生式右部的结尾')
				log_down()
		log('扫描得到的First集关系图: ', tc=-1)
		for k, v_set in first_relation.items():
			log(prd_fmt.format(k, ', '.join(sorted(v_set))))
		log('计算各First节点所能到达的终结符', tc=-1)
		firsts = dict()
		for k in self.table:
			firsts[k] = set()
			stack = [k]
			visited = set()
			log_up()
			while stack:
				c = stack.pop(-1)
				if c in visited:
					continue
				visited.add(c)
				for v in first_relation[c]:
					if v.isupper():
						if v not in visited:
							stack.append(v)
					else:
						firsts[k].add(v)
			log_down()
		for k, v in self.x.items():
			if v:
				firsts[k].add('')
		log('得到如下的各First集', tc=-1)
		for k, v_set in firsts.items():
			v_set = sorted(map(lambda _: _ or epsl, v_set))
			log(prd_fmt.format(k, ', '.join(v_set)))
		for k, v_list in self.table.items():
			for v in v_list:
				if v in firsts:
					continue
				first = {''}
				for c in v:
					if '' not in first:
						break
					first.remove('')
					first = first.union(firsts[c] if c.isupper() else {c})
				firsts[v] = first
		self.firsts = firsts

	@debug(0)
	def analyze_follows(self):
		self.show()
		log('开始扫描各产生式以构造First集关系图')
		follow_relation = {self.start: {'#'}}
		log_up()
		for k, v_list in self.table.items():
			for v in v_list:
				log('当前产生式: ' + prd_fmt.format(k, v or epsl), end='')
				if not any(c.isupper() for c in v):
					log(' \t(无非终结符, 跳过)')
					continue
				else:
					log()
				log_up()
				for i, c in enumerate(v):
					if not c.isupper():
						continue
					log('当前非终结符: {}'.format(c))
					log_up()
					j = 1
					while True:
						nxt = v[i+j:i+j+1]
						if nxt == '':
							log('已到达产生式结尾')
							log('故让Follow({})指向Follow({})'.format(c, k), tc=1)
							follow_relation.setdefault(c, set())
							follow_relation[c].add(k)
							break
						else:
							log('其后面第{}个字符为{}'.format(j, nxt))
							log_up()
							log('所以Follow({})指向First({})里的每个终结符'.format(c, nxt))
							follow_relation.setdefault(c, set())
							for t in self.firsts[nxt]:
								if t:
									follow_relation[c].add(t)
							if nxt.isupper() and self.x[nxt]:
								log('因为{}可以推出终结符'.format(nxt))
								log('故继续查看下一个字符')
								j += 1
							else:
								log('因为{}不能推出终结符'.format(nxt))
								log('故在当前产生式中对Follow({})的分析已经结束'.format(c))
								break
							log_down()
					log_down()
				log_down()
		log_down()
		log('扫描得到的Follow集关系图: ', tc=-1)
		for k, v_set in follow_relation.items():
			log(prd_fmt.format(k, ', '.join(sorted(v_set))))
		log('计算各Follows节点所能到达的终结符', tc=-1)
		follows = dict()
		for k in self.table:
			follows[k] = set()
			stack = [k]
			visited = set()
			log_up()
			while stack:
				c = stack.pop(-1)
				if c in visited:
					continue
				visited.add(c)
				for v in follow_relation[c]:
					if v.isupper():
						if v not in visited:
							stack.append(v)
					else:
						follows[k].add(v)
			log_down()
		log('得到如下的各Follow集', tc=-1)
		for k, v_set in follows.items():
			log(prd_fmt.format(k, ', '.join(v_set)))
		self.follows = follows
