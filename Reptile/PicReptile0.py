# -*- coding: UTF-8 -*-
import json
import os

import requests
from bs4 import BeautifulSoup


def download_barcode_images(search, keywords, save_path, images_num):
	# 创建保存图片的目录
	if not os.path.exists(save_path):
		os.makedirs(save_path)
	
	count = 0
	try:
		# 发送HTTP GET请求获取图片
		response1 = requests.get(search, params=keywords)
		
		if response1.status_code == 200:
			# 使用Beautiful Soup解析网页内容
			soup = BeautifulSoup(response1.text, 'html.parser')
			# 查找所有的<a>标签
			img_tags = soup.find_all('a')
			# 提取图片链接
			image_urls = []
			
			for img in img_tags:
				try:
					image_url = json.loads(img['m'])["murl"]
					image_urls.append(image_url)
					
					try:
						# 发送HTTP GET请求获取图片
						response = requests.get(image_url)
						
						if response.status_code == 200:
							# 从URL中提取文件名
							filename = os.path.join(save_path, os.path.basename(image_url))
							# 保存图片到本地
							with open(filename, 'wb') as f:
								f.write(response.content)
							
							count += 1
							print(f"Downloaded image {count}/{images_num}")
					except requests.exceptions.RequestException as e:
						print(f"Error: {str(e)}")
						pass
					finally:
						if count >= images_num:
							break
				except Exception as e:
					# print(e)
					pass
	
	# for image_url in image_urls:
	# try:
	# 	# 发送HTTP GET请求获取图片
	# 	response = requests.get(image_url)
	#
	# 	if response.status_code == 200:
	# 		# 从URL中提取文件名
	# 		filename = os.path.join(save_directory, f"barcode_{count}.jpg")
	# 		content = response.content
	# 		# 保存图片到本地
	# 		with open(filename, 'wb') as f:
	# 			f.write(content)
	#
	# 		count += 1
	# 		print(f"Downloaded image {count}/{num_images}")
	# except requests.exceptions.RequestException as e:
	# 	print(f"Error: {str(e)}")
	# 	pass
	# finally:
	# 	if count >= num_images:
	# 		break
	except requests.exceptions.RequestException as e:
		print(f"Error: {str(e)}")
		pass


url = "https://cn.bing.com/images/search?q="  # 替换为实际的图片URL
params = {
	'q'    : '工业场景 条码标签',
	'count': 200
}
save_directory = r"D:\Fenkx\Fenkx - General\AI\Dataset\01"  # 图片保存目录
num_images = 100  # 要下载的图片数量

download_barcode_images(url, params, save_directory, num_images)
