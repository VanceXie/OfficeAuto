import os
import hashlib


def group_files_by_size(directory):
	file_groups = {}
	for filename in os.listdir(directory):
		path = os.path.join(directory, filename)
		if os.path.isfile(path):
			size = os.path.getsize(path)
			if size in file_groups:
				file_groups[size].append(path)
			else:
				file_groups[size] = [path]
	return file_groups


def remove_duplicates(path, flag=0):
	'''
	:param path: 去重路径
	:param flag: 0，default，通过使用MD5散列值比较文件，耗费资源更多，比较更为严格；1，通过hash值比较文件，计算较快，稳定性相对较弱
	:return: unique_files列表
	'''
	# Step 1: Get the list of all files in the directory
	
	# Step 2: Group the files by size
	file_sizes = group_files_by_size(path)
	
	# Step 3-4: Deduplicate files with the same size
	for size in file_sizes:
		filenames = file_sizes[size]
		if len(filenames) > 1:
			unique_filenames = set()
			for filename in filenames:
				with open(os.path.join(path, filename), 'rb') as f:
					if flag == 0:
						file_hash = hashlib.md5(f.read()).hexdigest()
					elif flag == 1:
						file_hash = hash(f.read())
				if file_hash not in unique_filenames:
					unique_filenames.add(file_hash)
				else:
					filenames.remove(filename)
					os.remove(filename)
			file_sizes[size] = filenames
	
	# Step 5: Merge all the remaining files into a single list
	unique_files = []
	for size in file_sizes:
		unique_files.extend(file_sizes[size])
	
	return unique_files
