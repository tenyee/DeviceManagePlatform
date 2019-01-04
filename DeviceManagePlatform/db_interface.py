# -*- coding:utf-8 -*-
from django.http import HttpResponse
from DeviceInfo.models import DeviceInfo
from django.views.decorators.csrf import csrf_exempt
from DeviceInfo.models import DeviceInfo, GetObject
import json

def make_response(success, msg, code):
	ret = {}
	ret["success"] = success
	ret["msg"] = msg
	ret["code"] = code

	return json.dumps(ret)

#统一不同表的接口
g_model_info_dic = {
	"DeviceInfo" : [
		DeviceInfo.objects.filter,
		DeviceInfo.what,
		DeviceInfo.update,
		DeviceInfo.search_response,
		DeviceInfo.objects.all,
		GetObject
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
			##查询属性记录
			#filter_name = json_data['filter_name']
			#filter_value = json_data['filter_value']
			##获取要查询的表
			#model_name = json_data['model_name']
			#model_filter = get_model_filter(model_name)
			#model_what = get_model_what(model_name)
			##查询出记录
			#results = model_filter(**model_what(filter_name, filter_value))
			#更新相关属性值
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
			
	except:
		print("error occurs")

	return HttpResponse(ret)

@csrf_exempt
def add_items(request):
	try:
		ret = json.dumps({})

		if request.method == 'POST':
			json_data = json.loads(request.body)
			model_name = json_data['model_name']
			data_list = json_data['data_list']
			print("data_list:", data_list)
			for item in data_list:
				new_object = get_model_object(model_name)
				obj = new_object()
				obj.set(item)
				obj.save()
	except:
		pass

	return HttpResponse(ret)


















