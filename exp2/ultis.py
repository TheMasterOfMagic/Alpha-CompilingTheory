t_count = 0
line_feed = True
DEBUG = False


def debug(_debug):
	def outer_wrapper(func):
		def wrapper(*args, **kwargs):
			global DEBUG
			switched = False
			if _debug != DEBUG:
				DEBUG = _debug
				switched = True
			rv = func(*args, **kwargs)
			if switched:
				DEBUG = not _debug
			return rv
		return wrapper
	return outer_wrapper


def log(*args, **kwargs):
	global t_count, line_feed, DEBUG
	if DEBUG:
		tc = kwargs.pop('tc', 0)
		end = kwargs.get('end', '\n')

		t_count += tc
		if line_feed:
			print('\t'*t_count, end='')
		print(*args, **kwargs)
		t_count -= tc

		line_feed = '\n' in end


prd_fmt = '{} → {}'


def log_up(tc=1):
	global t_count
	t_count += tc


def log_down(tc=1):
	global t_count
	t_count -= tc


epsl = 'ϵ'
