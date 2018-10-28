from collections import OrderedDict
from grammar import Grammar


def main():
	e4_3 = OrderedDict(
		S=['aA', 'd'],
		A=['bAS', '']
	)
	e4_4 = OrderedDict(
		S=['aAS', 'b'],
		A=['bA', '']
	)
	e4_5 = OrderedDict(
		S=['AB', 'bC'],
		A=['', 'b'],
		B=['', 'aD'],
		C=['AD', 'b'],
		D=['aS', 'c'],
	)
	g = Grammar(e4_3)
	g.analyze_x()
	g.analyze_firsts()
	g.analyze_follows()
	g.analyze_selects()
	if g.is_ll1():
		g.determin_top_down('abd')


if __name__ == '__main__':
	main()
