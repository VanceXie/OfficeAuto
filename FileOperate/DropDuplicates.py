import datetime
import hashlib
import os
import shutil

import numpy as np

from tools import calculate_time
import cv2


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


# 余弦相似度计算
from PIL import Image
from numpy import average, dot, linalg


# 对图片进行统一化处理
def get_thum(image, size=(64, 64), greyscale=False):
	# 利用image对图像大小重新设置, Image.ANTIALIAS为高质量的
	image = image.resize(size, Image.Resampling.LANCZOS)
	if greyscale:
		# 将图片转换为L模式，其为灰度图，其每个像素用8个bit表示
		image = image.convert('L')
	return image


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


# image1 = Image.open(r'D:\vance\Downloads\知一妹妹\pics\0234.jpg')
# image2 = Image.open(r'D:\vance\Downloads\知一妹妹\pics\0235.jpg')
# cosin = image_similarity_vectors(image1, image2)
# print('图片余弦相似度', cosin)
def find_similar_images(folder_path, size: tuple):
	images_path = ([os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png")])
	# Use the images_path list to find similar images
	similar_images = []
	images = [(cv2.resize((cv2.imdecode(np.fromfile(image_path, np.uint8), 0)), size)).ravel() for image_path in images_path]
	corr_coef, res = image_similarity_vectors(images)
	
	for i in range(len(images_path)):
		for j in range(i + 1, len(images_path)):
			similarity = image_similarity_vectors(Image.open(images_path[i]), Image.open(images_path[j]))
			if similarity > 0.995:
				# Add the similar images to a list
				similar_images.append((images_path[i], images_path[j]))
	# Remove duplicate images from the list of similar images
	unique_images = list(set(sum(similar_images, ())))
	# Remove all but one image from each similar image group
	for i in range(len(unique_images)):
		for j in range(i + 1, len(unique_images)):
			if unique_images[i] in unique_images[j]:
				unique_images[j] = unique_images[j].replace(unique_images[i], "")
	# Remove empty strings from the list of similar images
	unique_images = [x for x in unique_images if x != ""]
	# Group similar images together
	similar_groups = []
	for image in unique_images:
		group = [x for x in unique_images if x.startswith(image)]
		if len(group) > 1:
			similar_groups.append(group)
	# Remove all but one image from each similar image group
	unique_groups = []
	for group in similar_groups:
		unique_groups.append((group[0],))
	# Convert the list of unique image groups to a list of similar image pairs
	similar_images = []
	for group in unique_groups:
		for i in range(len(group)):
			for j in range(i + 1, len(group)):
				similar_images.append((group[i], group[j]))
	return similar_images


def delete_similar_images(similar_images):
	for image_pair in similar_images:
		for image_path in image_pair:
			os.remove(image_path)
	print("Similar images deleted successfully.")


# # Example usage
# folder_path = r"D:\vance\Downloads\知一妹妹\pics"
# similar_images = find_similar_images(folder_path, (64, 64))
# print(similar_images)
# delete_similar_images(similar_images)
