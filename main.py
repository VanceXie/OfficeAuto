import os.path

from FileOperate import DropDuplicates, ReName
from FileOperate.Achieve import multithread_winrar_compress

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
	path = r"D:\Fenkx\Fenkx - General\AI\Dataset\BarCode\My Datasets\Test_Label\C12"
	DropDuplicates.remove_duplicates(path, 1, 1)
	pre = os.path.basename(path)
	ReName.rename_by_sort(path, 1, prefix=pre, fill_char='0', length=4)
# multithread_winrar_compress(path, 2, 128)
