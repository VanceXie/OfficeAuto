import winreg


def get_app_install_path(program_name: str) -> str:
	# 读取注册表
	with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as key:
		num_subkeys = winreg.QueryInfoKey(key)[0]
		i = 0
		while i < num_subkeys:
			try:
				# 读取子键名
				sub_key_name = winreg.EnumKey(key, i)
				# 打开子键
				with winreg.OpenKey(key, sub_key_name) as sub_key:
					# 读取子键值
					display_name = winreg.QueryValueEx(sub_key, 'DisplayName')[0]
					install_path = winreg.QueryValueEx(sub_key, 'InstallLocation')[0]
					if program_name.lower() in display_name.lower():
						return install_path
			except OSError:
				pass
			i += 1
		return None
