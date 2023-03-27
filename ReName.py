import os
import random
import re
import string


def rename_by_order(path: str, extension: str):
    # 列出目录下所有文件
    files = os.listdir(path)
    
    # 按照文件名排序
    # files.sort(key=lambda x: int(x.split('.')))
    files.sort(key=lambda l: int(re.findall('\d+', l)[0]))  # 找出字符串中的数字并依据其整形进行排序
    # 初始化计数器
    count = 1
    
    # 遍历文件并重命名
    for file in files:
        # 构造新文件名
        new_name = "{:0>2d}".format(count) + '.' + extension
        # 拼接路径和文件名
        src = os.path.join(path, file)
        dst = os.path.join(path, new_name)
        # 重命名文件
        os.rename(src, dst)
        # 计数器加一
        count += 1


def rename_by_size(path: str):
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


def rename_by_type(path: str, condition):
    # 遍历目录
    for root, dirs, files in os.walk(path):
        # 获取文件列表，并按文件大小排序
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
