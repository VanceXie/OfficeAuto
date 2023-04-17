from FileOperate import DropDuplicates, ReName
# import FileOperate
# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
	
	path = r"D:\vance\Downloads\BP3730-1\bbypchii\P"
	DropDuplicates.remove_duplicates(path, 0,1)
	ReName.rename_by_sort(path, '0', 3)
