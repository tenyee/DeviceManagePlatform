def task():
	import json,urllib.request as urllib
	#textmod={"model_name":"DeviceInfo","filter_name": "dev_ip", 'filter_value':'1.2.3.4','update_items':[['product_type', '##adfa#']]}
	textmod={"model_name":"DeviceInfo","data_list":[{"dev_ip":'abcd'}, {"dev_ip":"dddd"}],"filter_name": "dev_ip", 'filter_value':'1.2.3.4','update_items':[['product_type', '##adfa#']]}
	textmod = json.dumps(textmod)
	print(textmod)
	textmod = textmod.encode()
	#输出内容:{"params": {"password": "zabbix", "user": "admin"}, "jsonrpc": "2.0", "method": "user.login", "auth": null, "id": 1}
	header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',"Content-Type": "application/json"}
	url='http://127.0.0.1:8000/db/add_items'
	req = urllib.Request(url=url,data=textmod,headers=header_dict)
	res = urllib.urlopen(req)
	res = res.read()
	print(res)
