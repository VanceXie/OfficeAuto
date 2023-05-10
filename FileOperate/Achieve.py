import os
import tarfile
import threading
import zipfile


def get_name_and_path(url):
	url = os.path.normpath(url)
	# 获取路径的最后一层目录名
	# 获取文件名（带扩展名）
	name = os.path.basename(url)
	# 获取路径的上级目录（不包含最后一层目录）路径
	# 获取文件所在目录路径（不包含文件名）
	parent_directory_path = os.path.abspath(os.path.join(url, os.pardir))
	return name, parent_directory_path


def extract_files(folder_path, max_concurrent_files):
	file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.zip')]
	
	def extract_file(file_names_batch):
		for file_name in file_names_batch:
			with zipfile.ZipFile(file_name, 'r') as zip_ref:
				zip_ref.extractall()
	
	threads = []
	
	i = 0
	while i < len(file_names):
		file_names_batch = file_names[i:i + max_concurrent_files]
		t = threading.Thread(target=extract_file, args=(file_names_batch,))
		threads.append(t)
		i += max_concurrent_files
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	print('All files extracted successfully.')


def compress_files(folder_path, max_concurrent_files, dictionary_size, compression_format):
	file_urls = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
	
	def compress_file(file_urls_batch):
		for file_url in file_urls_batch:
			output_file_name = os.path.splitext(file_url)[0] + '.' + compression_format
			if compression_format == 'zip':
				with zipfile.ZipFile(output_file_name, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
					file_name = os.path.basename(file_url)
					password = os.path.splitext(file_name)[0]
					zip_file.setpassword(password.encode('utf-8'))
					zip_file.write(file_url, file_name)
					zip_file.close()
			elif compression_format == 'tar':
				with tarfile.open(output_file_name, 'w') as tar_file:
					tar_file.add(file_url)
			elif compression_format == 'tar.gz':
				with tarfile.open(output_file_name, 'w:gz') as tar_file:
					password = os.path.splitext(os.path.basename(file_url))[0]
					tar_file.add(file_url, compresslevel=3, filter=tarfile.Filter('gzip', '-%d' % dictionary_size))
			else:
				print('Unsupported compression format:', compression_format)
	
	threads = []
	i = 0
	while i < len(file_urls):
		file_urls_batch = file_urls[i:i + max_concurrent_files]
		t = threading.Thread(target=compress_file, args=(file_urls_batch,))
		threads.append(t)
		i += max_concurrent_files
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	print('All files compressed successfully.')


def winrar_compress(input_url, dict_size=64, rar=r'D:/Program Files/WinRAR'):
	"""
	注意路径和文件名中带空格的时候一定要多加一重引号！！
	:param input_url: 需要压缩的文件/文件夹名
	:param dict_size: 压缩字典大小
	:param rar: Rar路径，默认 rar_path='D:/Program Files/WinRAR'.
	:return:
	"""
	name_with_extension, parent_path = get_name_and_path(input_url)
	name_without_extension = os.path.splitext(name_with_extension)[0]
	
	password = '"' + name_without_extension + '"'
	_output_url = '"' + os.path.join(parent_path, name_without_extension) + '"'
	_input_url = '"' + input_url + '"'
	
	cmd_rar = rf'.\Rar.exe a -ep -hp{password} -md{dict_size} {_output_url} {_input_url}'
	# -ep 参数来指定不保存文件的父目录，-ep 参数必须放在 rar 命令行最前面
	
	os.chdir(rar)  # RaR切换工作目录
	result = os.system(cmd_rar)  # 执行压缩命令
	if result == 0:
		print('Successful Compress', input_url)
	else:
		print('FAILED Compress', input_url)


def winrar_uncompress(input_url, output_url=None, unrar=r'D:/Program Files/WinRAR'):
	"""
	:param input_url: 待解压文件的绝对路径
	:param output_url: 解压绝对路径, default None,解压到压缩文件所在路径
	:param unrar: unrar 程序的路径
	:return:
	"""
	name_with_extension, parent_path = get_name_and_path(input_url)
	name_without_extension = os.path.splitext(name_with_extension)[0]
	
	password = '"' + name_without_extension + '"'
	_input_url = '"' + input_url + '"'
	
	if output_url is None:
		_output_url = '"' + os.path.join(parent_path, name_without_extension) + '\\"'  # 默认解压到本路径
	else:
		_output_url = '"' + os.path.join(output_url, name_without_extension) + '\\"'
	
	cmd_unrar = rf'.\UnRAR.exe x -p{password} {_input_url} {_output_url}'
	'''
	因为使用CMD（Command Prompt）执行程序不能在程序全路径外直接加
	'''
	os.chdir(unrar)  # 切换到RaR.exe所在目录
	result = os.system(cmd_unrar)  # 执行压缩命令并返回执行状态
	# 判断是否执行成功
	if result == 0:
		print('Successful unCompress', input_url)
	else:
		print('FAILED unCompress', input_url)



# winrar_compress(r"D:\vance\Downloads\[BlackK studio]出生促進委員会～3分で受精完了～コスモ発情フラッシュ!!!1秒で発情即ハメ～逃げる隙も与えられない!!!")
winrar_uncompress(r"C:\Users\vance\Desktop\Temp\[BlackK studio]出生促進委員会～3分で受精完了～コスモ発情フラッシュ!!!1秒で発情即ハメ～逃げる隙も与えられない!!!.rar")
