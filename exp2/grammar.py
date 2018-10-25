from collections import OrderedDict
from copy import deepcopy
from ultis import *


class Grammar:
	def __init__(self, table: OrderedDict):
		# 取有序字典里第一个key作为起始状态
		start = tuple(table)[0]
		self.start, self.table = start, table

	def show(self):
		for k, v_list in self.table.items():
			for v in v_list:
				log(prd_fmt.format(k, v or epsl))

	def copy(self):
		return Grammar(deepcopy(self.table))

	def analyze_firsts(self):
		@debug(0)
		def analyze_epsilon_vn():
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
			return x
		print(analyze_epsilon_vn())
