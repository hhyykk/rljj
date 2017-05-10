#!/usr/bin/env python3
# -- coding: gb18030 --
import requests
import datetime
import time
import os
import sqlite3
import csv
import sys
import math
import threading
import pandas as pd
from wave import WaveData as wd
from win32.win32crypt import CryptUnprotectData
#用于从文件中获取Cookie
def get_cookie_from_chrome(host):
	cookiepath = os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"
	sql="select host_key,name,encrypted_value from cookies where host_key='%s'" % host
	with sqlite3.connect(cookiepath) as conn:
		cu = conn.cursor()
		cookies={name:CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()}
		return cookies
def get_Wave_Cookie():
	cookie = dict(cookies_are='guid=%s;key=%s;wave_session=%s;'%(get_cookie_from_chrome('.amap.com')['guid'],get_cookie_from_chrome('.amap.com')['key'],get_cookie_from_chrome('wave.xiaojukeji.com')['wave_session']))
	return cookie

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

def getResponse(url,param):
	print(param)
	return requests.get(url,params=param,cookies=get_Wave_Cookie(),headers=header)
TODAY_TIME=(datetime.datetime.now()-datetime.timedelta(1)).strftime('20%y-%m-%d')

def getDateRange(startTime,endTime):
	dateRange = []
	formatter = '20%y-%m-%d'
	s = datetime.datetime.strptime(startTime,formatter)
	e = datetime.datetime.strptime(endTime,formatter)
	delta = (e-s).days
	for i in range(delta+1):
		dateRange.append((s+datetime.timedelta(i)).strftime(formatter))
	return dateRange

def getOrderDetailInIdInDate(driver_id,thisdate):
	orders_number_group = getSomeoneOrderIdInThisDate(driver_id,thisdate)
	details_response_group = []
	for order_id in orders_number_group:
		try:
			details_response_group.append(fetchOrderId(order_id))
		except:
			continue
	return details_response_group
	
def getSomeoneOrderIdInThisDate(driver_id,thisdate):
	print('downloading%sin%s orders'%(driver_id,thisdate))
	order_list_url='http://wave.xiaojukeji.com/v2/app/order/driverorderlbslist'
	payload={
		'date':thisdate,
		'driver_id':driver_id
	}
	r = getResponse(order_list_url,payload)
	orders = []
	errno = r.json()['errno']
	if errno == '0':
		data = r.json()['data']['data']
		for d in data:
			orders.append(d['order_id'])
		return orders
	else:
		print(r.json()['error'])
		return orders
def fetchOrderId(order_id):
	print(order_id)
	order_detail_url='http://wave.xiaojukeji.com/v2/app/order/orderdetail'
	r = getResponse(order_detail_url,{'order_id':order_id})
	if r.json()['errno'] != '0':
		print(r.json()['error'])
	return r
		
def writeAllOrderToCsv():
	w=None
	count = 0
	with open('unpayorder.csv','w') as f:
		for detail_group in wave.getUnpayOrder():
			for detail in detail_group:
				if count == 0:
					count +=1 
					w = csv.DictWriter(f,detail.keys())
					w.writeheader()
					w.writerow(detail)
				else:
					w.writerow(detail)

	
def writeOrderToCsv(driver_id,stime,etime=TODAY_TIME):
	dateRange = getDateRange(stime,etime)
	orderss = []
	orderdetails=[]
	for date in dateRange:
		orders = getSomeoneOrderInThisDate(driver_id,date)
		for order in orders:
			orderdetails.append(fetchOrderId(order))
	print(orderdetails[0].keys())
	with open(driver_id+'order.csv','w',newline='') as f:
		w = csv.DictWriter(f,fieldnames=orderdetails[0].keys())
		w.writeheader()
		for order in orderdetails:
			w.writerow(order)
def getFrontDate(delta=7):
	return (datetime.datetime.now()-datetime.timedelta(delta)).strftime('20%y-%m-%d')
	

	
def writeToExcel(responses):
	filename = datetime.datetime.now().strftime('20%y-%m-%d%H%M%S')+'.csv'
	with open(filename,'w',newline='') as f:
		count = 0
		w=None
		print(type(responses))
		if type(responses) == list:
			for r in responses:
				print(type(r))
				#if it is response
				if type(r) == requests.models.Response:
					try:
						data = r.json()['data']['data']
						for d in data:
							if count == 0:
								w=csv.DictWriter(f,d.keys())
								w.writeheader()
								w.writerow(d)
								count +=1
							else:
								w.writerow(d)
					except:
						print(r.text)
				#if it is list
				elif type(r) == list:
					try:
						for d in r:
								if count == 0:
									w=csv.DictWriter(f,d.keys())
									w.writeheader()
									w.writerow(d)
									count +=1
								else:
									w.writerow(d)
					except:
						print(r.text)
				elif type(r) == dict:
					if count == 0:
						count+=1
						w = csv.DictWriter(f,r.keys())
						w.writeheader()
						w.writerow(r)
					else:
						w.writerow(r)
	return filename
							
def getTimeDelta(startTime,endTime):
	s = datetime.datetime.strptime(startTime,'20%y-%m-%d')
	e = datetime.datetime.strptime(endTime,'20%y-%m-%d')
	return (e-s).days
						
def getSomeoneTponeDataDetail(driver_id,start_time=TODAY_TIME,end_time=TODAY_TIME):
	url = 'http://wave.xiaojukeji.com/v2/app/record/gettponedatadetail'
	payload = {
		'size':str(getTimeDelta(start_time,end_time)+1),
		'items':'serve_score,coplaint_cnt,bad_star_cnt,dcancel_cnt,pcancel_cnt,badstar_percent,fivestar_percent,serve_level,online_time,serve_time,pay_charge_time,drawout_distance,sum_normal_distance,finish_cnt,pay_order_cnt,finish_flow,pay_flow,finish_flow_avg,pay_flow_avg,assign_listen_cnt,assign_finish_cnt,pay_flow_avg,assign_finish_percent,morning_peak_finish_cnt,night_peak_finish_cnt,normal_peak_finish_cnt',
		'form_type':'1',
		'start_time':start_time,
		'end_time':end_time,
		'page':'1'
		}
	payload['driver_id'] = driver_id
	return getResponse(url,payload)
		
def getAllDriverId():
	driver_id_group = []
	for r in getDriverListInManager():
		data = r.json()['data']['data']
		for d in data:
			driver_id_group.append(d['driver_id'])
	return driver_id_group
		
def appendKeyValue(dict,key,Value):
	dict[key] = Value
	return dict
		
def getAllTponeDataDetail(start_time=TODAY_TIME,end_time=TODAY_TIME):
	tponedatadetail_group = []
	for response in getDriverListDataResponses():
		data = response.json()['data']['data']
		for d in data:
			id = d['driver_id']
			name = d['name']
			org = d['deparment']
			r = getSomeoneTponeDataDetail(id,start_time,end_time)
			tpone = r.json()['data']['data']
			tpone[0]['driver_id']=id
			tpone[0]['name']=name
			tpone[0]['org']=org
			tponedatadetail_group.append(tpone)
	return tponedatadetail_group
		
def getAllTponeDataDetailWriteToCsv(start_time=TODAY_TIME,end_time=TODAY_TIME):
	writeToExcel(getAllTponeDataDetail())
						
						
def getDataResponse(url,params):
	FirstResponse = getResponse(url,params)
	error = FirstResponse.json()['error']
	Responses=[]
	if error != '':
		print(error.decode('utf-8'))
	else:
		data = FirstResponse.json()['data']
		count = data['count']
		if count <= 100:
			params['size']='100'
			FirstResponse = getResponse(url,params)
			Responses.append(FirstResponse)
		else:
			PAGE_MAX = int(math.ceil(data['count']/100)) + 1
			for page in range(1,PAGE_MAX):
				params['page'] = str(page)
				params['size'] = '100'
				Responses.append(getResponse(url,params))
		return Responses
			
def getDriverListDataResponses():
	Response = []
	url="http://wave.xiaojukeji.com/v2/dc/driverdiagnosis/driverlist"
	r = getResponse(url,{'size':'100','model':'5'})
	data = r.json()['data']
	if data['count'] == 0:
		print(data['notice'])
		r = getResponse(url,{'size':'100','model':'5','date':TODAY_TIME})
	if int(data['count']) <=100:
		Response.append(r)
	else:
		PAGE_MAX = int(math.ceil(data['count']/100)) + 1
		for page in range(1,PAGE_MAX):
			r = getResponse(url,{'size':'100','model':'5','page':str(page)})
			Response.append(r)
		return Response
		
def getDriverListInManager():
	Response = []
	url="https://wave.xiaojukeji.com/v2/app/drivermanager/driverlist"
	r = getResponse(url,{'size':'100','bind_status':'1'})
	data = r.json()['data']
	if int(data['count']) <=100:
		Response.append(r)
	else:
		PAGE_MAX = int(math.ceil(data['count']/100)) + 1
		for page in range(1,PAGE_MAX):
			r = getResponse(url,{'size':'100','bind_status':'1','page':str(page)})
			Response.append(r)
		return Response
		
def getOrder(date = getFrontDate()):
	details_group_group = []
	for d in WaveData.getDriverManagerDriverList():
		details_group_group.append(getOrderDetailInIdInDate(d['driver_id'],date))
	return details_group_group

def writeUnpayOrderToExcel(detail_group_group,filename = getFrontDate(),*,getUnpay = True):
	count = 0
	w=None
	with open(filename+'unpayorder.csv','w',newline='') as f:
		for detail_group in detail_group_group:
			for detail in detail_group:
				try:
					data = detail.json()['data']
				except Exception as e:
					print(e)
					continue
				if count == 0:
					count=2
					w = csv.DictWriter(f,data.keys())
					w.writeheader()
					w.writerow(data)
				else:
					try:
						w.writerow(data)
					except Exception as e:
						print(e)
						continue
	if getUnpay:
		driverlist = wd.getDiagnositcData()
		unpay_order_group = getUnpayOrder()
		with open(filename+'仁林锦江'+'7日未垫付.csv','w',newline ='') as f:
				w = csv.DictWriter(f,['序号','司机姓名','司机电话','订单号','司机ID','城市','case描述（须填写订单时间，对12.1之前的订单标黄）','专/快/企/其他','核实结果','备注'])
				w.writeheader()
				count =1
				for order in unpay_order_group:
					name = ''
					phone = ''
					logs_info = eval(order['logs'])[-2]
					name = logs_info['l_infos'][1]['value']
					phone = logs_info['l_infos'][0]['value']
					w.writerow({'序号':str(count),
					'司机姓名':name,
					'司机电话':phone,
					'订单号':'`'+order['order_id'],
					'司机ID':'`'+order['driver_id'],
					'城市':'深圳',
					'case描述（须填写订单时间，对12.1之前的订单标黄）':order['begincharge_time']+'  从  '+order['s_address']+'  到  '+order['e_address'],
					'专/快/企/其他':'快车',
					'核实结果':'',
					'备注':''})
					count +=1
def getUndianfuOrder(*,date = getFrontDate()):
	driverlist = wd.getDiagnositcData()
	unpay_order_group = getUnpayOrder(order_filename=date+'unpayorder.csv')
	with open('仁林锦江'+date+'7日未垫付.csv' ,'w',newline ='') as f:
			w = csv.DictWriter(f,['序号','司机姓名','司机电话','订单号','司机ID','城市','case描述（须填写订单时间，对12.1之前的订单标黄）','专/快/企/其他','核实结果','备注'])
			w.writeheader()
			count =1
			for order in unpay_order_group:
				name = ''
				phone = ''
				logs_info = eval(order['logs'])[-2]
				name = logs_info['l_infos'][1]['value']
				phone = logs_info['l_infos'][0]['value']
				w.writerow({'序号':str(count),
				'司机姓名':name,
				'司机电话':phone,
				'订单号':'`'+order['order_id'],
				'司机ID':'`'+order['driver_id'],
				'城市':'深圳',
				'case描述（须填写订单时间，对12.1之前的订单标黄）':order['begincharge_time']+'  从  '+order['s_address']+'  到  '+order['e_address'],
				'专/快/企/其他':'快车',
				'核实结果':'',
				'备注':''})
				count +=1
	
def downloadOrder():
	writeUnpayOrderToExcel(getOrder())
	
def _getDriverLBS():
	url = 'http://wave.xiaojukeji.com/v2/app/order/driverorderlbslist'
	driver_lbs_group = []
	for response in getDriverListInManager():
		driverlist = response.json()['data']['data']
		for d in driverlist:
			id  = d['driver_id']
			name = d['name']
			r = getResponse(url,{'driver_id':id})
			try:
				monitor = r.json()['data']['monitor']
				monitor['name']=name
				driver_lbs_group.append(monitor)
			except:
				print(r.text)
				continue
	return driver_lbs_group
		
def writeDriverLbsToCsv(driver_lbs_group):
	filename = 'driverlbs.csv'
	count = 0
	w=None
	with open(filename,'w',newline='') as f:
		for driver_lbs in driver_lbs_group:
			if count == 0:
				count =2
				w = csv.DictWriter(f,driver_lbs.keys())
				w.writeheader()
				w.writerow(driver_lbs)
			else:
				w.writerow(driver_lbs)
				
def getDriverLBSListAndWriteToExcel():
	filepath = writeDriverLbsToCsv(_getDriverLBS())
	return filepath
def isEdge(driver):
	redDelta = float(driver['total_charge_time']) - float(driver['redline_charge_time'])
	if redDelta < 0 :
		if redDelta > -8:
			return True
	else:
		return False

		
def getEdgeDriver():
	EdgeDriver_group = []
	for r in getDriverListDataResponses():
		data = r.json()['data']['data']
		for d in data:
			if isEdge(d) == True:
				EdgeDriver_group.append(d)
	return EdgeDriver_group
	
def isCloseCar(monitor):
	if monitor['status'].encode('gbk') == b'\xca\xd5\xb3\xb5':
		return True
	else:
		return False
	
	
def getDriverLbs(driver_group):
	url = 'http://wave.xiaojukeji.com/v2/app/order/driverorderlbslist'
	driver_lbs_group = []
	for d in driver_group:
		dictMerged = d.copy()
		driver_lbs_response = getResponse(url,{'driver_id':d['driver_id']})
		driver_lbs_monitor = driver_lbs_response.json()['data']['monitor']
		if isCloseCar(driver_lbs_monitor) == True:
			dictMerged.update(driver_lbs_monitor)
			driver_lbs_group.append(dictMerged)
	print('line346',len(driver_lbs_group))
	return driver_lbs_group

def getEdgeDriverAndWriteToCsv():
	writeToExcel(getDriverLbs(getEdgeDriver()))
	
def getUnpayOrder(*,order_filename = getFrontDate()+'unpayorder.csv',fee_min=40):

	with open(order_filename,'r') as f:
		reader = csv.DictReader(f)
		UnpayOrder_group = []
		for row in reader:
			if row['pay_name'] =='未支付':
				if float(row['fee'])>=fee_min:
					UnpayOrder_group.append(row)
		ordered_UnpayOrder_group = sorted(UnpayOrder_group,key = lambda x:float(x['fee']),reverse=True)
		return ordered_UnpayOrder_group

		
		