import os
import zipfile
import tarfile
import rarfile
import threading


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


compress_files(r"D:\vance\Downloads", 3, None, 'zip')
