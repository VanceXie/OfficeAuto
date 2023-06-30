import os.path

from FileOperate import DropDuplicates, ReName
from FileOperate.Achieve import multithread_winrar_compress

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
	path = r"D:\Fenwick\Videos"
	# DropDuplicates.remove_duplicates(path, 1, 1)
	# # pre = os.path.basename(path)+'_'
	# ReName.rename_by_sort(path, 1, prefix='', fill_char='0', length=3)
	# ReName.rename_prefix_or_suffix(path, '[铃木美咲Misaki Suzuki]', '', ' ')
	multithread_winrar_compress(path, 27, 64, 2)
