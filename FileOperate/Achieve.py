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


def compress(input_url, dict_size=64, rar_path=r'D:\Develop\OfficeAuto\FileOperate\Rar.exe'):
	"""
	:param dict_size: 压缩字典大小
	:param input_url: 需要压缩的文件/文件夹名,这里时名字如果时某个文件夹下的所有文件则直接写:input_fileName="."
	:param output_url: 压缩文件的输出路径及其压缩的文件名; 如 output_file ="d:/test/test.rar"
	:param intput_path: 要压缩的文件夹路径信息
	:param rar_path: WinRar软件路径，默认 rar_path='C:/"Program Files"/WinRAR/WinRAR.exe'.注意路径和文件名中带空格的时候一定要多加一重引号！！
	"""
	name, parent_path = get_name_and_path(input_url)
	name_without_extension = os.path.splitext(name)[0]
	
	_output_url = '"' + name_without_extension + '"'
	_input_url = '"' + name + '"'
	cmd_command = f'{rar_path} a -hp{_output_url} -md{dict_size} {_output_url} {_input_url}'
	os.chdir(parent_path)  # WinRaR切换工作目录
	result = os.system(cmd_command)  # 执行压缩命令
	if result == 0:
		print('Successful Compress', input_url)
	else:
		print('FAILED Compress', input_url)


def win_rar_uncompress(compressed, filepath, unrar='"./UnRAR.exe"'):
	"""
	:param compressed: 待解压文件的绝对路径
	:param filepath: 解压后文件存放的文件夹，绝对路径
	:param unrar: unrar 程序的路径
	:return:
	"""
	# 由于参数全部都是绝对路径，所以无需切换工作目录，直接执行解压命令即可
	# 注意：所有路径不需要在外层添加双引号，否则可能导致解压失败
	uncompress = f'{unrar} x {compressed} {filepath}'
	state = os.system(uncompress)  # 执行压缩命令并返回执行状态
	# 判断是否执行成功
	assert state == 0, '解压失败'


# file_name, parent_path = get_name_and_path(r"D:\vance\Downloads")
# output_url = os.path.join(parent_path, file_name + '.rar')
# print(file_name)
# print(parent_path)
compress(r'D:\vance\Downloads\[BlackK studio]出生促進委員会～3分で受精完了～コスモ発情フラッシュ!!!1秒で発情即ハメ～逃げる隙も与えられない!!!')
