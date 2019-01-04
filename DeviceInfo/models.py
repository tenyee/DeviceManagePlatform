# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.
class DeviceInfo(models.Model):
	verbose_name = '设备信息'

	dev_ip       = models.CharField('设备IP',max_length = 128)
	product_type = models.CharField('产品形态',max_length = 64)
	name         = models.CharField('设备帐号',max_length = 32, default = 'szhw')
	passwd       = models.CharField('设备密码', max_length = 32, default = 'Changeme_123')

	dev_linux_ip = models.CharField('linux主机', max_length = 128)
	linux_passwd = models.CharField('linux密码', max_length = 32)
	linux_name   = models.CharField('linux帐号', max_length = 32)

	location     = models.CharField('设备位置', max_length = 128)
	update_time  = models.CharField('设备信息更新时间', max_length = 32)
	status       = models.CharField('设备连接状态', max_length = 16, default = 'fail')

	def what(field, value):
		if field == 'dev_ip':
			return {'dev_ip':value}
		else:
			return None

	#查询返回
	def search_response(records):
		data_source = []
		columns = []
		result = {}
		#构造列表项
		columns.append({"title":"设备ip", "dataIndex":"dev_ip", "key":"dev_ip"})
		columns.append({"title":"产品形态", "dataIndex":"product_type", "key":"product_type"})
		columns.append({"title":"linux主机", "dataIndex":"dev_linux_ip", "key":"dev_linux_ip"})
		columns.append({"title":"设备位置", "dataIndex":"location", "key":"location"})
		columns.append({"title":"设备信息更新时间", "dataIndex":"update_time", "key":"update_time"})
		columns.append({"title":"设备连接状态", "dataIndex":"status", "key":"status"})

		for record in records:
			item = {}
			item["dev_ip"] = record.dev_ip
			item["product_type"] = record.product_type
			item["dev_linux_ip"] = record.dev_linux_ip
			item["location"] = record.location
			item["update_time"] = record.update_time
			item["status"] = record.status
			data_source.append(item)

		result["dataSource"] = data_source
		result["columns"] = columns

		return result

	def set(self, data):
		self.dev_ip = data["dev_ip"]

	#注意哪些可更新，哪些不行的
	def update(self, field, value):
		if field == 'dev_ip':
			self.dev_ip = value
		elif field == 'product_type':
			self.product_type = value
		elif field == 'name':
			self.name = value
		elif field == 'passwd':
			self.passwd = value
		elif field == 'dev_linux_ip':
			self.dev_linux_ip = value
		elif field == 'linux_passwd':
			self.linux_passwd = value
		elif field == 'linux_name':
			self.linux_name = value
		elif field == 'location':
			self.location = value
		elif field == 'update_time':
			self.update_time = value
		elif field == 'status':
			self.status = value

		self.save()

	def __str__(self):
		return '%s' %(self.dev_ip)

	def __unicode__(self):
		return self.verbose_name

	class Meta:
		verbose_name = '设备信息'
		verbose_name_plural = '设备信息表'

def GetObject():
	return DeviceInfo()