#coding: utf-8
import requests
from enum import Enum
import datetime 
import math
import wave
import time
import os
from win32.win32crypt import CryptUnprotectData
import sqlite3

SERVE_SCORE = 'serve_score'
COPLAINT_CNT = 'coplaint_cnt'
BAD_STAR_CNT = 'bad_star_cnt'
DCANCEL_CNT = 'dcancel_cnt'
PCANCEL_CNT = 'pcancel_cnt'
BADSTAR_PERCENT = 'badstar_percent'
FIVESTAR_PERCENT = 'fivestar_percent'
SERVE_LEVEL = 'serve_level'
ONLINE_TIME = 'online_time'
SERVE_TIME = 'serve_time'
PAY_CHARGE_TIME = 'pay_charge_time'
DRAWOUT_DISTANCE = 'drawout_distance'
SUM_NORMAL_DISTANCE = 'sum_normal_distance'
FINISH_CNT = 'finish_cnt'
PAY_ORDER_CNT = 'pay_order_cnt'
	


START_TIME_INDEX = 0
END_TIME_INDEX = 1
def get_cookie_from_chrome(host):
	cookiepath = os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"
	sql="select host_key,name,encrypted_value from cookies where host_key='%s'" % host
	with sqlite3.connect(cookiepath) as conn:
		conn.execute('PRAGMA busy_timeout = 3000')
		cu = conn.cursor()
		cookies={name:CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()}
		return cookies
def get_Wave_Cookie():
	cookie = dict(cookies_are='guid=%s;key=%s;wave_session=%s;'%(get_cookie_from_chrome('.amap.com')['guid'],get_cookie_from_chrome('.amap.com')['key'],get_cookie_from_chrome('wave.xiaojukeji.com')['wave_session']))
	return cookie

def getToday():
	return datetime.datetime.now().strftime('20%y-%m-%d')
def getYesterday():
	return (datetime.datetime.now()-datetime.timedelta(1)).strftime('20%y-%m-%d')
def getTheDayBeforeYesterday():
	return (datetime.datetime.now()-datetime.timedelta(2)).strftime('20%y-%m-%d')
def getResponse(url,params):
	header={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	'Accept':'application/json, text/javascript, */*; q=0.01',
	'Connection':'keep-alive',
	'Host':'wave.xiaojukeji.com',
	'Referer':'https://wave.xiaojukeji.com/v2/',
	'Accept':'application/json, text/plain, */*',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Connection':'keep-alive'
	}
	print(params)
	r = requests.get(url,cookies=get_Wave_Cookie(),headers=header,params=params,verify=False)
	r = requests.get(url,cookies=get_Wave_Cookie(),headers=header,params=params,verify = False)
	return r

		
def getWaveResponse(url,params):
	header={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	'Accept':'application/json, text/javascript, */*; q=0.01',
	'Connection':'keep-alive',
	'Host':'wave.xiaojukeji.com',
	'Referer':'https://wave.xiaojukeji.com/v2/',
	'Accept':'application/json, text/plain, */*',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Connection':'keep-alive'
	}
	print(params)
	FIRST_RESPONSE = requests.get(url,cookies=get_Wave_Cookie(),headers=header,params=params,verify=False)
	SIZE_MAX = math.ceil(FIRST_RESPONSE.json()['data']['count']/100)
	data = []
	if SIZE_MAX==1:
		data = FIRST_RESPONSE.json()['data']['data']
	else:
		data+=FIRST_RESPONSE.json()['data']['data']
		
		for page in range(2,SIZE_MAX+1):
			params['page'] = str(page)
			r = getResponse(url,params)
			data+=r.json()['data']['data']
	return data
	
def getDriverManagerDriverList():
	drivers_list = []
	url = 'http://wave.xiaojukeji.com/v2/app/drivermanager/driverlist'
	payload = {'size':'100','page':'1','join_model':'5'}
	FIRST_RESPONSE  = getResponse(url,payload)
	SIZE_MAX = math.ceil(FIRST_RESPONSE.json()['data']['count']/100)
	if SIZE_MAX==1:
		drivers_list = FIRST_RESPONSE.json()['data']['data']
	else:
		drivers_list+=FIRST_RESPONSE.json()['data']['data']
		
		for page in range(2,SIZE_MAX+1):
			payload['page'] = str(page)
			r = getResponse(url,payload)
			drivers_list+=r.json()['data']['data']
	return drivers_list
	
def getTimeDelta(startTime,endTime):
	s = datetime.datetime.strptime(startTime,'20%y-%m-%d')
	e = datetime.datetime.strptime(endTime,'20%y-%m-%d')
	return str((e-s).days)
def data_types_to_str(data_types):
	string = ''
	for data_type in data_types:
		string += (data_type+',')
	return string[0:-1]
#params:data_type,driver_id,dates(start_time,end_time),form_type,1,2,3=day,week,month
def getDriverData(driver_id,*data_types,form_type='1',start_time,end_time=getYesterday()):
	payload = {
		'form_type':form_type,
		'start_time':start_time,
		'end_time':end_time,
		'driver_id':driver_id,
		'size':getTimeDelta(start_time,end_time),
		'items':data_types_to_str(data_types)
	}
	r = getResponse('http://wave.xiaojukeji.com/v2/app/record/gettponedatadetail',payload)
	errno = r.json()['errno']
	if errno == '0':
		data = r.json()['data']['data']
		return data
	else:
		return r.json()['error']
	
	
#def getOrgData(data_type,org_id,dates):
#	if data_type == SERVE_SCORE:
#		
#	elif data_type == COMPLAINT:
#		
#	elif data_type == COMMENT:
#	elif data_type == FINISH_ORDER:
#	elif data_type == DRIVERLIST:
#	elif data_type == DRIVER_MANAGER:
#	elif data_type == CAR_MANAGER:
#	elif data_type == ONLINE_DRIVER:
#	elif data_type == ORDER_GROUP:

#def getAllDriverData(data_type):
	
def getOrgstree():
	r = getResponse('http://wave.xiaojukeji.com/v2/app/org/orgstree',{})
	data = r.json()['data']
	return data
	
def getDiagnositcData(*,date=getToday(),payload = {}):
	url = 'http://wave.xiaojukeji.com/v2/dc/driverdiagnosis/driverlist'
	data = []
	
	payload['size'] = '100'
	payload['model'] = '5'
	payload['date'] = date
	
	r = getResponse(url,payload)
	print(r)
	count = r.json()['data']['count']
	if int(count) <=100:
		return r.json()['data']['data']
	else:
		data = r.json()['data']['data']
		SIZE_MAX = math.ceil(count/100)+1
		for page in range(2,SIZE_MAX):
			payload['page'] = str(page)
			r = getResponse(url,payload)
			data += r.json()['data']['data']
			return data

	
	
	
			
def IsRed(phone):
	day = datetime.datetime.now().day
	max = 5*(day - 1)
	r = getResponse('http://wave.xiaojukeji.com/v2/dc/driverdiagnosis/driverlist',{'phone':phone})
	if r.json()['errno'] != '0':
		print(r.json()['error'])
		return '已解绑'
	else:
		if len(r.json()['data']['data']) == 0:
			return 'what'
		if r.json()['data']['data'][0]['serve_level'] == '--':
			delta = str(round(float(r.json()['data']['data'][0]['charge_hours'])-max,1))
			return '未达成,差'+delta+'h'
		else:
			return '达成'
def IsA(phone,Min_AScore):
	r = getResponse('http://wave.xiaojukeji.com/v2/dc/driverdiagnosis/driverlist',{'phone':phone})
	if r.json()['errno'] != '0':
		print(r.json()['error'])
		return '已解绑'
	else:
		if r.json()['data']['data'][0]['serve_level'] == 'A':
			return '达成'
		else:
			delta = str(round(float(r.json()['data']['data'][0]['serve_score']) - float(Min_AScore),3))
			return '未达成,差'+delta+'分'
			
def getOrgDataInfo(date = getYesterday()):
	url = 'http://wave.xiaojukeji.com/v2/dc/driversurvey/orgdatainfo'
	r = getResponse(url,{'start_time':date,'end_time':date})
	data = r.json()['data']
	return data
	
def getTopTen(column):
	kw = {
		'serve_score':'服务分',
		'finish_flow':'完成流水',
	}
	Top_url = 'https://wave.xiaojukeji.com/v2/dc/driversurvey/toptenlist'
	payload ={
		'start_time':getYesterday(),
		'end_time':getYesterday(),
		'page':'1',
		'size':'10',
		'order_column':column,
	}
	r = getResponse(Top_url,payload)
	top_ten_list = r.json()['data']['data']
	print(type(top_ten_list))
	return top_ten_list	
			
def getCompanyData(data_type,*,date = getYesterday(),params_plus={}):
	data = getOrgDataInfo()
	
	print(data_type)
	if data_type == '入围率':
		return data['standard_rate']
	elif data_type == 'A档率':
		return data['level_a_rate']
	elif data_type == '入围率环比':
		print( data['compare_standard'])
		if data['compare_standard'][0:1] =='-':
			return '下降' +data['compare_standard']
		elif data['compare_standard'] =='0.00%':
			return '没变'
		else:
			return '上升'+ data['compare_standard']
	elif data_type == 'A档率环比':
		if data['compare_level_a_rate'][0:1] == '-':
			return '下降'+data['compare_level_a_rate']
		elif data['compare_level_a_rate'] =='0.00%':
			return '没变'
		else:
			return '上升'+data['compare_level_a_rate']
			
	elif data_type =='文字好评':
		text_orders = []
		url = 'http://wave.xiaojukeji.com/v2/dc/ordercomplaint/orderlist'
		payload = dict({'org_id':'4367','size':'1000'},**params_plus)
		
		r = getResponse(url,payload)
		data = r.json()['data']['data']
		ORDER_SIZE_MAX = math.ceil(float(r.json()['data']['count']/100))
		print(len(data))
		for d in data:
			if d['comment'] != '':
				text_orders.append(d)
		if ORDER_SIZE_MAX > 1:
			for page in range(2,ORDER_SIZE_MAX+1):
				payload['page'] = str(page)
				r = getResponse(url,payload)
				data = r.json()['data']['data']
				for d in data:
					if d['comment'] != '':
						text_orders.append(d)
		return text_orders
	elif data_type == '投诉':
		payload = dict({'order_type':'2','page':'1','parent_org_id':'-1','size':'100'},**params_plus)
		r = getResponse('http://wave.xiaojukeji.com/v2/dc/ordercomplaint/complaintlist',payload)
		return r.json()['data']['data']
	elif data_type == '差评':
		text_orders = []
		url = 'http://wave.xiaojukeji.com/v2/dc/ordercomplaint/orderlist'
		payload = dict({'comment':'1','order_type':'2','page':'1','parent_org_id':'-1','star':'1,2,3','size':'1000'},**params_plus)
		
		r = getResponse(url,payload)
		data = r.json()['data']['data']
		ORDER_SIZE_MAX = math.ceil(float(r.json()['data']['count']/100))
		print(len(data))
		for d in data:
			if d['comment'] != '':
				text_orders.append(d)
		if ORDER_SIZE_MAX > 1:
			for page in range(2,ORDER_SIZE_MAX+1):
				r = getResponse(url,payload)
				data = r.json()['data']['data']
				for d in data:
					if d['comment'] != '':
						text_orders.append(d)
		return text_orders
	elif data_type == '昨日入围目标司机':
		day = datetime.datetime.now().day
		if day ==1:
			return '没有入围目标司机'
		else:
			charginghours_min = 5*(day - 3)
			charginghours_max = 5*(day - 2)
			YesterdayTargetDrivers = getDiagnositcData(date = getYesterday(),payload = {'charginghours_min':str(charginghours_min),'charginghours_max':str(charginghours_max)})
			target_drivers = ''
			for d in YesterdayTargetDrivers:
				target_drivers +='\t'+ d['name']+'('+IsRed(d['phone'])+')'+ '\n'
			return target_drivers
	elif data_type == '昨日A档目标司机':
		AScore = float(input('今天A档服务分？'))
		YesterdayATargetDrivers = getDiagnositcData(date = getYesterday(),payload ={'serve_level':'20','order_type':'2','order_column':'serve_score'})
		target_drivers = ''
		SIZE = len(YesterdayATargetDrivers)
		Top = int(round(SIZE/4,3))
		for i in range(Top):
			target_drivers+='\t'+YesterdayATargetDrivers[i]['name']+'('+IsA(YesterdayATargetDrivers[i]['phone'],AScore )+')'+'\n'
		return target_drivers
	elif data_type == '今日主要事项':
		return '1.日常数据分析'
	elif data_type == '明日目标司机':
		target_drivers  = '\t'
		for d in getDiagnositcData(payload={'size':'100','page':'1'}):
			if int(d['redline_rate'][0:-1]) < 100: 	
				if float(d['redline_distance']) < 5 :
					target_drivers+=(' '+d['name'])
		return target_drivers
	elif data_type == '明日A档目标司机':
		target_drivers  = '\t'
		DriverList = getDiagnositcData(payload={'serve_level':'20','order_type':'2','order_column':'serve_score'})
		SIZE = len(DriverList)
		Top = int(round(SIZE/4,3))
		for i in range(Top):
			target_drivers+=' '+DriverList[i]['name']
		return target_drivers
	elif data_type == '完成流水TOP10':
		return getTopTen('finish_flow')
	elif data_type == '服务分TOP10':
		return getTopTen('serve_score')