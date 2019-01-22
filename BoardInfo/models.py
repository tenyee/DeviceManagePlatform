from django.db import models
import sys
import os
from Base import BaseModel, Utils

# Create your models here.
class BoardInfo(models.Model, BaseModel.BaseModel):
	verbose_name = '单板信息'

	board_type = models.CharField('单板类型', max_length = 32)
	board_present = models.CharField('在位状态', max_length = 32)
	board_register = models.CharField('注册状态', max_length = 32)
	board_where = models.CharField('所在设备', max_length = 32)
	board_slot = models.CharField('所在槽位', max_length = 4)

	#查询返回
	def search_response(records):
		data_source = []
		columns = []
		result = {}
		#构造列表项
		columns.append({"title":"单板类型", "dataIndex":"board_type", "key":"board_type"})
		columns.append({"title":"在位状态", "dataIndex":"board_present", "key":"board_present"})
		columns.append({"title":"注册状态", "dataIndex":"board_register", "key":"board_register"})
		columns.append({"title":"所在设备", "dataIndex":"board_where", "key":"board_where"})
		columns.append({"title":"所在槽位", "dataIndex":"board_slot", "key":"board_slot"})


		for record in records:
			item = {}
			item["board_type"] = record.board_type
			item["board_present"] = record.board_present
			item["board_register"] = record.board_register
			item["board_where"] = record.board_where

			data_source.append(item)

		result["dataSource"] = data_source
		result["columns"] = columns

		return result

	def what(field, value):
		if field == 'board_where':
			return {'board_where':value}
		else:
			return None

	def set(self, data):
		if data == None or data == {}:
			return 

		self.board_type 	= Utils.get_value(data, "board_type")
		self.board_present  = Utils.get_value(data, "board_present")
		self.board_register = Utils.get_value(data, "board_register")
		self.board_where 	= Utils.get_value(data, "board_where")
		self.board_slot     = Utils.get_value(data, "board_slot")


	def __str__(self):
		return '%s' %(self.board_type)

	def __unicode__(self):
		return self.verbose_name

	class Meta:
		verbose_name = '单板信息'
		verbose_name_plural = '单板信息表'

def GetObject():
	return BoardInfo()