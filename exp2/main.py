from collections import OrderedDict
from grammar import Grammar


def main():
	g = Grammar(OrderedDict(
		S=['AB', 'bC'],
		A=['', 'b'],
		B=['', 'aD'],
		D=['aS', 'c'],
		C=['AD', 'b'],
	))
	g.analyze_x()
	g.analyze_firsts()
	g.analyze_follows()


if __name__ == '__main__':
	main()
