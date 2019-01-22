#通过函数

#获取字典中的属性值
def get_value(data_list, name):
	if data_list == None or data_list == {}:
		print("[Utils:get_value]failed to get value, reason:data_list == None or data_list == {}")
		return "None"

	if name not in data_list:
		print("[Utils:get_value]failed to get value, reason:data_list[%s] == None" %name)
		return "None"

	return data_list[name]

