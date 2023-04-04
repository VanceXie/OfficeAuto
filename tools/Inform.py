import time


def print_time(func):
	def wrapper(*args, **kwargs):
		print("Function {} is running...".format(func.__name__))
		start_time = time.time()
		result = func(*args, **kwargs)
		end_time = time.time()
		print("Function {} is finished. Time taken: {:.4f}s".format(func.__name__, end_time - start_time))
		return result
	
	return wrapper
