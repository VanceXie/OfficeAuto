import os
import re
from tools import *


def rename_by_sort(path: str, fill_char: str = '0', length: int = 3):
	"""
	:param path: path of files
	:param fill_char: char of filling before filename，default ‘0’
	:param length: length of filename，default 3
	:return: None
	"""
	# 列出目录下所有文件
	filenames = os.listdir(path)
	
	# 按照文件名排序
	filenames.sort(key=str.lower)
	
	# 遍历文件并重命名
	for index, filename in enumerate(filenames):
		# 构造新文件名
		new_filename_no_extension = "{:{fill_char}>{length}}".format(index + 1, fill_char=fill_char, length=length)
		extension = filename.split('.')[-1].lower()
		new_filename = '{}.{}'.format(new_filename_no_extension, extension)
		# 拼接路径和文件名
		src = os.path.join(path, filename)
		dst = os.path.join(path, new_filename)
		# 重命名文件
		os.rename(src, dst)


@print_time
def rename_by_num(path: str, num_loc: int = 0, fill_char: str = '0', length: int = 3):
	"""
	:param num_loc: 根据字符串中的第几组连续数字进行排序，default 0
	:param path: path of files
	:param fill_char: char of filling before filename，default ‘0’
	:param length: length of filename，default 3
	:return: None
	"""
	# 列出目录下所有文件
	filenames = os.listdir(path)
	
	# 按照文件名中的数字排序
	filenames.sort(key=lambda l: int(re.findall('\d+', l)[num_loc]))  # 找出字符串中的第一组连续数字并依据其整形进行排序
	
	# 遍历文件并重命名
	for index, filename in enumerate(filenames):
		# 构造新文件名
		new_filename_no_extension = "{:{fill_char}>{length}}".format(index + 1, fill_char=fill_char, length=length)
		extension = filename.split('.')[-1].lower()
		new_filename = '{}.{}'.format(new_filename_no_extension, extension)
		# 拼接路径和文件名
		src = os.path.join(path, filename)
		dst = os.path.join(path, new_filename)
		# 重命名文件
		os.rename(src, dst)


@print_time
def rename_by_size(path: str):
	"""
	:param path:
	:return:
	"""
	# 列出目录下所有文件
	files = os.listdir(path)
	
	# 获取文件大小并按照文件大小排序
	files.sort(key=lambda x: os.path.getsize(os.path.join(path, x)))
	
	# 初始化计数器
	count = 1
	
	# 遍历文件并重命名
	for file in files:
		__filename, extension = os.path.splitext(file)
		
		new_name = str(count) + extension
		
		# 如果新文件名已存在，则在文件名后面添加数字
		j = 1
		while os.path.exists(os.path.join(path, new_name)):
			# 构造新文件名
			new_name = f'{count}_{j}.{extension[1:]}'
			j += 1
		# 拼接路径和文件名
		src = os.path.join(path, file)
		dst = os.path.join(path, new_name)
		# 重命名文件
		os.rename(src, dst)
		# 计数器加一
		count += 1


@print_time
def rename_by_type(path: str, condition):
	# 遍历目录
	for root, dirs, files in os.walk(path):
		# 获取文件列表，并排序
		files = sorted(files, key=condition)
		
		# 遍历文件
		for i, file in enumerate(files):
			# 获取文件类型和路径
			file_type = file.split('.')[-1].lower()
			file_path = os.path.join(root, file)
			
			# 获取文件名前缀和新文件名
			prefix = file_type
			new_file_name = f'{prefix}_{i + 1}.{file_type}'
			
			# 如果新文件名已存在，则在文件名后面添加数字
			j = 1
			while os.path.exists(os.path.join(root, new_file_name)):
				new_file_name = f'{prefix}_{i + 1}_{j}.{file_type}'
				j += 1
			
			# 重命名文件
			os.rename(file_path, os.path.join(root, new_file_name))
