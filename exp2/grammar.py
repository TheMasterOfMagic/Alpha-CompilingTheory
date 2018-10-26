from collections import OrderedDict
from copy import deepcopy
from ultis import *


class Grammar:
	def __init__(self, table: OrderedDict):
		# 取有序字典里第一个key作为起始状态
		start = tuple(table)[0]
		self.start, self.table = start, table
		self.firsts = None

	def show(self):
		for k, v_list in self.table.items():
			for v in v_list:
				log(prd_fmt.format(k, v or epsl))

	def copy(self):
		return Grammar(deepcopy(self.table))

	@debug(0)
	def analyze_epsilon_vn(self):
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
			return x

	@debug(0)
	def analyze_firsts(self):
		x = self.analyze_epsilon_vn()
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
					if c.islower() or not x[c]:
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
		log('逐个计算并消除仅指向终结符的节点', tc=-1)
		firsts = dict((k, set()) for k in first_relation)
		while first_relation:
			for k, v_set in first_relation.items():
				if not any(map(str.isupper, v_set)):
					log('非终结符{}目前不指向任何非终结符'.format(k))
					log('将{}并入First[{}]中'.format(', '.join(sorted(v_set)), k), tc=1)
					firsts[k] = firsts[k].union(v_set)
					log('并将First[{}]并入所有指向{}的节点'.format(k, k))
					log_up()
					for k_, v_set_ in first_relation.items():
						if k in v_set_:
							log('节点{}指向了节点{}'.format(k_, k))
							log('合并结果，并删除此边', tc=1)
							firsts[k_] = firsts[k_].union(firsts[k])
							first_relation[k_].remove(k)
					log('最后删除节点{}'.format(k))
					log_down()
					first_relation.pop(k)
					break
		else:
			log_down()
			log('First集关系图已空')
			log('各非终结符的First集已计算完毕')
		for k, v in x.items():
			if v:
				firsts[k].add('')
		for k, v_set in firsts.items():
			v_set = set(v if v else epsl for v in v_set)
			log('{}: ({})'.format(k, ', '.join(v_set)))
		self.firsts = firsts
