from FileOperate import DropDuplicates, ReName
from FileOperate.Achieve import multithread_winrar_compress


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
	path = r"D:\vance\Music"
	# DropDuplicates.remove_duplicates(path, 0, 1)
	# ReName.rename_by_sort(path, 150, '0', 4)
	multithread_winrar_compress(path, 2, 128)
