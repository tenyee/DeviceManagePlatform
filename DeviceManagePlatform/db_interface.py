# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

#-------------新数据添加区
from DeviceInfo.models import DeviceInfo
from DeviceInfo.models import GetObject as DeviceInfoGetObject

from BoardInfo.models import BoardInfo
from BoardInfo.models import GetObject as BoardInfoGetObject

#统一不同表的接口
g_model_info_dic = {
	"DeviceInfo" : [
		DeviceInfo.objects.filter,
		DeviceInfo.what,
		DeviceInfo.update,
		DeviceInfo.search_response,
		DeviceInfo.objects.all,
		DeviceInfoGetObject
		],

	"BoardInfo" : [
		BoardInfo.objects.filter,
		BoardInfo.what,
		BoardInfo.update,
		BoardInfo.search_response,
		BoardInfo.objects.all,
		BoardInfoGetObject
		],

}

def get_model_filter(model_name):
	return g_model_info_dic[model_name][0] 

def get_model_what(model_name):
	return g_model_info_dic[model_name][1]

def get_model_update(model_name):
	return g_model_info_dic[model_name][2]

def get_model_search_response(model_name):
	return g_model_info_dic[model_name][3]

def get_model_all(model_name):
	return g_model_info_dic[model_name][4]

def get_model_object(model_name):
	return g_model_info_dic[model_name][5]


#----------------------------------
def make_response(success, msg, code):
	ret = {}
	ret["success"] = success
	ret["msg"] = msg
	ret["code"] = code

	return json.dumps(ret)

def get_model_data_records(json_data):
	#查询属性记录
	filter_name = json_data['filter_name']
	filter_value = json_data['filter_value']
	#获取要查询的表
	model_name = json_data['model_name']
	model_filter = get_model_filter(model_name)
	model_what = get_model_what(model_name)
	#查询出记录
	results = model_filter(**model_what(filter_name, filter_value))

	return results

#设备信息更新
#格式 textmod={"model_name":"DeviceInfo","filter_name": "dev_ip", 'filter_value':'1.2.3.4','update_items':[['product_type', '##adfa#']]}
@csrf_exempt
def update(request):
	try:
		ret = make_response(False, 'None', 0)

		if request.method == 'POST':
			json_data = json.loads(request.body)
			results = get_model_data_records(json_data)
			update_items = json_data['update_items']
			for dev in results:
				print('id:', dev.id)
				for item in update_items:
					dev.update(*item)

			print(results)

		else:
			ret = make_response(False, 'use POST method', 123)

	except DeviceInfo.DoesNotExist:
			ret = make_response(False, 'update item : %s is not exist' %(filter_name), 123)
	except :
			ret = make_response(False, 'please check the paramters that you pass to the server', 404)

	return HttpResponse(ret.encode())

############################################
#函数名：search
#说明：返回某个表的所有记录
#格式：http://ip:port/db/search?model_name=DeviceInfo

@csrf_exempt
def search(request):
	try:
		ret = json.dumps({})

		if request.method == 'GET':
			model_name = request.GET.get("model_name")
			print("model_name:", model_name)
			search_response = get_model_search_response(model_name)
			get_all_records = get_model_all(model_name)
			records = get_all_records()
			
			data = search_response(records)
			ret = json.dumps(data)
			
	except Exception as e:
		print("[search]failed to search, reason:", str(e), str(Exception))

	return HttpResponse(ret)

############################################
#函数名：add_items
#说明：添加记录,先把老的全删除
#格式：
# {
# 	"model_name": "DeviceInfo",
# 	"data_list": [{
# 		"dev_ip": "abcd"
# 	}, {
# 		"dev_ip": "dddd"
# 	}],
# 	"filter_name": "dev_ip",
# 	"filter_value": "1.2.3.4"
# }
#model_name   表的名字
#data_list    添加的数据项
#filter_name  过滤属性
#filter_value 属性值
@csrf_exempt
def add_items(request):
	try:
		ret = json.dumps({})

		if request.method == 'POST':
			json_data = json.loads(request.body)
			model_name = json_data['model_name']
			data_list = json_data['data_list']
			print("data_list:", data_list)
			#先以指定字段删除所有选项
			get_model_data_records(json_data).delete()

			for item in data_list:
				#获取创建对象接口
				new_object = get_model_object(model_name)
				#创建对象
				obj = new_object()
				#调用接口设置属性
				obj.set(item)
				#保存
				obj.save()

	except Exception as e:
		print("[add_items]failed to add_items, reason:", str(e), str(Exception))
		ret = json.dumps({"success":False, "msg":"Something error occurs"})

	return HttpResponse(ret)


















