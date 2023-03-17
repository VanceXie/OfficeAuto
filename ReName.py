import os


def rename_by_order(path: str, extension: str):
    # # 指定目录路径
    # path = "path/to/directory"
    
    # 列出目录下所有文件
    files = os.listdir(path)
    
    # 按照文件名排序
    files.sort(key=lambda x: int(x.split('.')[0][3:-1]))
    
    # 初始化计数器
    count = 1
    
    # 遍历文件并重命名
    for file in files:
        # 构造新文件名
        new_name = str(count) + '.' + extension
        # 拼接路径和文件名
        src = os.path.join(path, file)
        dst = os.path.join(path, new_name)
        # 重命名文件
        os.rename(src, dst)
        # 计数器加一
        count += 1
