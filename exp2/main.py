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
	g = Grammar(h4_4, 'E')
	g.analyze_x()
	g.analyze_firsts()
	g.analyze_follows()
	g.analyze_selects()
	print(g.is_ll1())


if __name__ == '__main__':
	main()
