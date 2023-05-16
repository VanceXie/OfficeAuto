import datetime
import hashlib
import os
import shutil

from tools import calculate_time


def movefile(srcfile, dstdir):  # 移动函数
	if not os.path.isfile(srcfile):
		print("%s not exist!" % (srcfile))
	else:
		fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
		if not os.path.exists(dstdir):
			os.makedirs(dstdir)  # 创建路径
		dsypath = os.path.join(dstdir, fname)
		shutil.move(srcfile, dsypath)  # 移动文件
		print("move %s -> %s" % (srcfile, dsypath))


def group_files_by_size(directory):
	file_groups = {}
	filenames = os.listdir(directory)
	dir_num = 0
	for filename in filenames:
		path = os.path.join(directory, filename)
		if os.path.isfile(path):
			size = os.path.getsize(path)
			if size in file_groups:
				file_groups[size].append(path)
			else:
				file_groups[size] = [path]
		else:
			dir_num += 1
	print(f'去重前文件个数：{len(filenames) - dir_num}；去重前目录个数：{dir_num}')
	return file_groups


@calculate_time
def remove_duplicates(path: str, compare_flag: int = 0, delete_flag: int = 0):
	"""
	
	:param path: 去重路径
	:param compare_flag: 0，default，通过使用MD5散列值比较文件，耗费资源更多，比较更为严格；1，通过hash值比较文件，计算较快，稳定性相对较弱
	:param delete_flag: delete_flag: 是否直接删除重复文件。default 0，则不删除仅集中放入“duplicates_datetime”文件夹；1，直接删除
	:return: unique_files列表
	"""
	
	# Step 2: Group the files by size
	file_sizes = group_files_by_size(path)
	
	# Step 3-4: Deduplicate files with the same size
	for size in file_sizes:
		filenames = file_sizes[size]
		if len(filenames) > 1:
			unique_filenames = set()
			for filename in filenames:
				with open(os.path.join(path, filename), 'rb') as f:
					if compare_flag == 0:
						file_hash = hashlib.md5(f.read()).hexdigest()
					elif compare_flag == 1:
						file_hash = hash(f.read())
				if file_hash not in unique_filenames:
					unique_filenames.add(file_hash)
				else:
					filenames.remove(filename)
					if delete_flag == 1:
						os.remove(filename)  # 删除文件
					else:
						movefile(os.path.join(path, filename), os.path.join(path, 'duplicates_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')))  # 移动文件
			file_sizes[size] = filenames
	
	# Step 5: Merge all the remaining files into a single list
	unique_files = []
	for size in file_sizes:
		unique_files.extend(file_sizes[size])
	print(f'去重后文件个数：{len(unique_files)}')
	return unique_files
