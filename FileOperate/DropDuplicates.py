import datetime
import hashlib
import os
import shutil

import numpy as np
from numpy import linalg

from tools import calculate_time


def movefile(srcfile, dst_dir):  # 移动函数
	if not os.path.isfile(srcfile):
		print("%s not exist!" % srcfile)
	else:
		filepath, filename = os.path.split(srcfile)  # 分离文件名和路径
		if not os.path.exists(dst_dir):
			os.makedirs(dst_dir)  # 创建路径
		dst_path = os.path.join(dst_dir, filename)
		shutil.move(srcfile, dst_path)  # 移动文件
		print("move %s -> %s" % (srcfile, dst_path))


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


# 计算图片的余弦距离
def image_similarity_vectors(images):
	"""
	:param images: 二维列表，每一行代表拉成一维的图片
	:return: corr_coef,相关系数; res,图片间的点积
	"""
	# 求每个图片间的相关系数
	corr_coef = np.corrcoef(images)
	# 求图片的范数
	norms = np.linalg.norm(images, axis=1)
	images_norms = images / norms[:, np.newaxis]
	# dot返回的是点积，对二维数组（矩阵）进行计算
	res = np.dot(images_norms, images_norms.T)
	return corr_coef, res
