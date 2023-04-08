from FileOperate import DropDuplicates, ReName
# import FileOperate
# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
	
	path = r"D:\ProgramData\Temp\RJ310551"
	DropDuplicates.remove_duplicates(path, 0,1)
	# ReName.rename_by_num(path, 0, '0', 3)
	
	# ReName.rename_by_size(r'C:\Users\fy.xie\Desktop\stereo_img\2000w_12\left')
