#coding:utf-8
import requests
import datetime
import time
import csv
import sys
import math
import pandas as pd
import wave
from wave import WaveData as wd
import writeYeJiBang as yjb
#用于从文件中获取Cookie
FileCookie=open('WaveCookie.txt','r').read()
cookie=dict(cookies_are=FileCookie)
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
	return wd.getResponse(url,param)
TODAY_TIME=(datetime.datetime.now()-datetime.timedelta(1)).strftime('20%y-%m-%d')

class DriverData():
	def __init__(self,d1,d2,d3,d4):
		self.d1 = d1
		self.d2 = d2
		self.d3 = d3
		self.d4 = d4

#获取服务分
def getServeScore(name,time=TODAY_TIME):
	url='http://wave.xiaojukeji.com/v2/dc/statisticservescore/driverinfo'
	r = getResponse(url,{'start_time':time,'end_time':time,'name':name})
	return r
#获取好评
def getComment(name,time=TODAY_TIME):
	url='http://wave.xiaojukeji.com/v2/dc/statisticscomment/driverinfo'
	r = getResponse(url,{'start_time':time,'end_time':time,'name':name})
	return r
#获取红线进度
def getDiagnosis(name,time=TODAY_TIME):
	url="http://wave.xiaojukeji.com/v2/dc/driverdiagnosis/driverlist"
	r = getResponse(url,{'name':name})
	return r
#获取完成流水
def getFinishOrder(name,time=TODAY_TIME):
	url='http://wave.xiaojukeji.com/v2/dc/finishorder/driver'
	r = getResponse(url,{'start_time':time,'end_time':time,'name':name})
	return r
#获取司机名单
def getDriverListDataResponses():
	Response = []
	url="http://wave.xiaojukeji.com/v2/dc/driverdiagnosis/driverlist"
	r = getResponse(url,{'size':'100','model':'5'})
	data = r.json()['data']
	if int(data['count']) <=100:
		Response.append(r)
	else:
		PAGE_MAX = int(math.ceil(data['count']/100)) + 1
		for page in range(1,PAGE_MAX):
			r = getResponse(url,{'size':'100','model':'5','page':str(page)})
			Response.append(r)
		return Response

def fetchD(d,time):
	d1 = getFinishOrder(d['name'],time).json()['data']['data']
	d2 = getComment(d['name'],time).json()['data']['data']
	d3 = getServeScore(d['name'],time).json()['data']['data']
	if len(d1) == 0:
		return None
	else:
		d1 = d1[-1]
		
	if len(d2) == 0:
		return None
	else:
		d2 = d2[-1]
	
	if len(d3) == 0:
		return None
	else:
		d3 = d3[-1]
	d4 = d
	return DriverData(d1,d2,d3,d4)		
	
def getDatesRange(start_time,delta):
	dates = []
	stime = datetime.datetime.strptime(start_time,'20%y-%m-%d')
	for i in range(delta,0,-1):
		dates.append((stime-datetime.timedelta(i)).strftime('20%y-%m-%d'))
	dates.append(start_time)
	return dates
print(getDatesRange(TODAY_TIME,2))
def getData(time = TODAY_TIME):
	Drivers=[]
	responses = getDriverListDataResponses()

	count = 0
	for r in responses:
		data = r.json()['data']
		list = data['data']
		TotalCount = data['count']
		for d in list:
			pass
	return Drivers
def writeToExcel(startTime = TODAY_TIME,delta=0):
	print('你要获取的数据的时间是',getDatesRange(startTime,delta))
	responses  = getDriverListDataResponses()
	print('正在写入Excel')
	with open('finishOrder_Score_complaint.csv', 'w',newline='') as fp:
		fieldnames=['日期','姓名','流水金额','完成单数','在线时长','服务时长','计费时长','服务里程','计费里程','服务分','档位','低星差评','投诉','部门','总计费时长','红线时长','红线进度','距红线','本月目标时长','本月达标进度','日期','姓名','平均星级','评价订单数','一星','二星','三星','四星','五星','五星占比','低星率']
		writer=csv.DictWriter(fp,fieldnames=fieldnames)
		writer.writeheader()
		#获取时间序列
		dates = getDatesRange(startTime,delta)

			#遍历时间序列
		for startTime in dates:
				#获取司机名单
			
			count = 1
			for response in responses:
				TotalCount = response.json()['data']['count']
				listData = response.json()['data']['data']
				for d in listData:
					print(d['name'],count,'/',TotalCount)
					count+=1
					driverdata = fetchD(d,startTime)
					if driverdata == None:
						print(driverdata)
						continue
					d1 = driverdata.d1
					d2 = driverdata.d2
					d3 = driverdata.d3
					d4 = driverdata.d4
					
					level = d3['level']
					complaint_count = d3['complaint_count']
					if level == '':
						level = 0
					if complaint_count == '':
						complaint_count=0
					
					writer.writerow({'日期':d1['date'],'姓名':d1['name'],'流水金额':d1['finish_flowfee'],'完成单数':d1['finish_finish_cnt'],'在线时长':d1['finish_online_time'],'服务时长':d1['finish_serve_time'],'计费时长':d1['finish_fee_time'],'服务里程':d1['finish_serve_distance'],'计费里程':d1['finish_work_distance'],'服务分':d3['serve_score'],'档位':level,'低星差评':d3['low_star_comment'],'投诉':complaint_count,'部门':d4['deparment'],'总计费时长':d4['total_charge_time'],'红线时长':d4['redline_charge_time'],'红线进度':d4['redline_rate'],'距红线':d4['redline_distance'],'本月目标时长':d4['target_charge_time'],'本月达标进度':d4['target_rate'],'评价订单数':d2['comment_count'],'平均星级':d2['avg_star'],'一星':d2['one_star'],'二星':d2['two_star'],'三星':d2['three_star'],'四星':d2['four_star'],'五星':d2['five_star'],'五星占比':d2['five_star_percent'],'低星率':d2['low_star_percent']})

def downloadDriverSpyData():
	data = []
	data1 = wd.getDiagnositcData(date=wd.getYesterday())
	data2 = wd.getDiagnositcData(payload={})
	data1 = sorted(data1,key = lambda x:int(x['redline_rate'][0:-1]),reverse=True)
	rank = 0
	for d in data1:
		rank+=1
		d['rank'] = str(rank)
		d['date'] = wd.getTheDayBeforeYesterday()
	data2 = sorted(data2,key = lambda x:int(x['redline_rate'][0:-1]),reverse=True)
	rank = 0
	for d in data2:
		d['date'] = wd.getYesterday()
		rank+=1
		d['rank'] = str(rank)
	data +=data2
	data +=data1

	count = 0 
	w = None
	with open('spydata.csv','w',newline='') as f:
		w = csv.DictWriter(f,['日期','司机姓名','服务分','昨日累计计费时长','红线时长','距红线','距红线排序','档位'])
		w.writeheader()
		for d in data:
			w.writerow({
			'日期':d['date'],
			'司机姓名':d['name'],
			'服务分':d['serve_score'],
			'昨日累计计费时长':d['charge_hours'],
			'红线时长':d['redline_charge_time'],
			'距红线':d['redline_distance'],
			'距红线排序':d['rank'],
			'档位':d['serve_level']
			})

def DailyReport():				
	r = ''
	
	r += wd.getToday()+'仁林锦江日报:\n'
	r += '本月目标：激活司机数150，入围率80%，A档率50%\n'
	r += '一、日常数据：\n'
	r += '1.入围率'+wd.getCompanyData('入围率')+'环比昨日'+wd.getCompanyData('入围率环比')+'，A档率'+wd.getCompanyData('A档率')+'环比昨日'+wd.getCompanyData('A档率环比')+'\n'
	r += '2.昨日目标完成情况：\n'
	r += ' (1)入围率目标完成情况:\n'
	r += '  ' + wd.getCompanyData('昨日入围目标司机')+'\n'
	r += ' (2)A档率目标完成情况:\n'
	r += '  ' + wd.getCompanyData('昨日A档目标司机') + '\n'
	r += '二、今日主要事项:\n'
	r += ' '+wd.getCompanyData('今日主要事项')+'\n'
	r += '三、明日工作计划:\n'
	r += ' (1)明日入围目标司机:\n'
	r += ' '+wd.getCompanyData('明日目标司机')+'\n'
	r += ' (2)明日A档目标司机:\n'
	r += ' '+wd.getCompanyData('明日A档目标司机')+'\n'
	
	with open(wd.getToday()+'daily.txt','w') as f:
		f.write(r)
	
	
#print(wd.getCompanyData('昨日入围目标司机'))
def getCMD():
	cmd = input('''输入指令：
	1.下载今日数据
	2.下载某日数据
	3.下载前几天到今天的数
	4.司机位置和时间
	5.下载未支付订单
	6.下载某人某月的订单数据
	7.下载司机监控表数据
	8.下载服务评价
	9.今日日报生成
	10.下载司机名单
	11.流水TOP10
	12.服务分TOP10
	13.获取司机计费时长和当前状态
	14.今日业绩报表
	15.统计报表数据
	> ''')
	if cmd == '1':
		writeToExcel()
	elif cmd == '2':
		cmd2 = input('请输入日期>')
		writeToExcel(cmd2)
	elif cmd == '3':
		cmd3 = input('请输入几天前>')
		
		cmd31 = input('你要获取的数据的时间是%s%s'%(getDatesRange(TODAY_TIME,int(cmd3)),'? 确定按1 重新选择按输入2>'))
		if cmd31 == '1':
			writeToExcel(TODAY_TIME,int(cmd3))
		elif cmd31 == '2':
			getCMD()
	elif cmd =='4':
		wave.getEdgeDriverAndWriteToCsv()
	elif cmd == '5':
		wave.downloadOrder()
	elif cmd == '6':
		driver_id = input('请输入司机id>')
		date = input('请输入日期>')
		orderid_group = wave.getSomeoneOrderIdInThisDate(driver_id,date)
		order_detail_group = []
		for order_id in orderid_group:
			order_detail_group.append(wave.fetchOrderId(order_id))
		with open(driver_id+date+'.csv','w',newline='') as f:
			count = 0
			w=None
			for order_detail_response in order_detail_group:
				order_detail = order_detail_response.json()['data']
				if count == 0:
					w = csv.DictWriter(f,order_detail.keys())
					count +=1
					w.writeheader()
					w.writerow(order_detail)
				else:
					w.writerow(order_detail)
		print('%s在%s的订单下载完成'%(driver_id,date))
	elif cmd == '7':
		downloadDriverSpyData()
	elif cmd == '8':
		cmd81 = input('1.好评\n2.差评\n3.投诉\n')
		if cmd81 == '1':
			cmd811 = input('今天的还是以前的？\n1.以前的\n2.今天的')
			if cmd811 == '2':
				with open('text_orders.csv','w',newline='') as f:
					text_order_group = wd.getCompanyData('文字好评')
					w = csv.DictWriter(f,['姓名','队伍','城市','开始时间','结束时间','评价时间','订单类型','星级','评价内容'])
					w.writeheader()
					for order in text_order_group:
						try:
							w.writerow({'姓名':order['name'],
							'队伍':order['org_route'],
							'城市':order['city_name'],
							'开始时间':order['strived_time'],
							'结束时间':order['finish_time'],
							'评价时间':order['comment_time'],
							'订单类型':order['order_validity'],
							'星级':order['star'],
							'评价内容':order['comment'].encode('utf-8').decode('utf-8', errors='ignore')})
						except Exception as e:
							print(e)
							continue
			else:
				cmd811 = input('请输入日期\n')
				with open(cmd811+'text_orders.csv','w',newline='') as f:
					text_order_group = wd.getCompanyData('文字好评',params_plus={'start_time':cmd811,'end_time':cmd811})
					w = csv.DictWriter(f,['姓名','队伍','城市','开始时间','结束时间','评价时间','订单类型','星级','评价内容'])
					w.writeheader()
					for order in text_order_group:
						try:
							w.writerow({'姓名':order['name'],
							'队伍':order['org_route'],
							'城市':order['city_name'],
							'开始时间':order['strived_time'],
							'结束时间':order['finish_time'],
							'评价时间':order['comment_time'],
							'订单类型':order['order_validity'],
							'星级':order['star'],
							'评价内容':order['comment'].encode('utf-8').decode('utf-8', errors='ignore')})
						except Exception as e:
							print(e)
							continue
		elif cmd81 == '2':
			cmd811 = input('今天的还是以前的？\n1.以前的\n2.今天的\n')
			if cmd811 == '2':
				with open('text_orders.csv','w',newline='') as f:
					text_order_group = wd.getCompanyData('差评')
					w = csv.DictWriter(f,['姓名','队伍','城市','开始时间','结束时间','评价时间','订单类型','星级','评价内容'])
					w.writeheader()
					for order in text_order_group:
						try:
							w.writerow({'姓名':order['name'],
							'队伍':order['org_route'],
							'城市':order['city_name'],
							'开始时间':order['strived_time'],
							'结束时间':order['finish_time'],
							'评价时间':order['comment_time'],
							'订单类型':order['order_validity'],
							'星级':order['star'],
							'评价内容':order['comment'].encode('utf-8').decode('utf-8', errors='ignore')})
						except Exception as e:
							print(e)
							continue
			elif cmd811 == '1':
				cmd8111 = input('请输入日期\n>')
				with open(cmd8111+'star123text_orders.csv','w',newline='') as f:
					text_order_group = wd.getCompanyData('差评',params_plus={'start_time':cmd8111,'end_time':cmd8111})
					w = csv.DictWriter(f,['姓名','队伍','城市','开始时间','结束时间','评价时间','订单类型','星级','评价内容'])
					w.writeheader()
					for order in text_order_group:
						try:
							w.writerow({'姓名':order['name'],
							'队伍':order['org_route'],
							'城市':order['city_name'],
							'开始时间':order['strived_time'],
							'结束时间':order['finish_time'],
							'评价时间':order['comment_time'],
							'订单类型':order['order_validity'],
							'星级':order['star'],
							'评价内容':order['comment'].encode('utf-8').decode('utf-8', errors='ignore')})
						except Exception as e:
							print(e)
							continue
				
		elif cmd81 == '3':
			cmd813 = input('今天的还是以前的?\n1.以前的\n2.今天的\n>')
			if cmd813 == '2':
				payload = {}
			elif cmd813 =='1':
				cmd8111 = input('请选择日期>')
				payload = {'start_time':cmd8111,'end_time':cmd8111}
			with open('complaint.csv','w',newline='') as f:
					complaints = wd.getCompanyData('投诉',params_plus = payload)
					w = csv.DictWriter(f,['订单号','司机姓名','司机手机号','部门','城市','接单时间','订单完成时间','投诉时间','投诉分类','投诉详情'])
					w.writeheader()
					for c in complaints:
						try:
							w.writerow({
							'订单号':c['order_id'],
							'司机姓名':c['name'],
							'司机手机号':c['phone'],
							'部门':c['org_name'],
							'接单时间':c['strived_time'],
							'订单完成时间':c['finish_time'],
							'投诉时间':c['complaint_time'],
							'投诉分类':c['complaint_type'],
							'投诉详情':c['complaint_info'],
							})
						except Exception as e:
							print(e)
							continue
		else:
			getCMD()
	elif cmd == '9':
		DailyReport()
	elif cmd =='10':
		cmd101 = input('选择日期  1.%s  2.%s>\n'%(wd.getYesterday(),wd.getToday()))
		if cmd101 == '1':
			data = wd.getDiagnositcData(date = wd.getYesterday())
		elif cmd101 == '2':
			data = wd.getDiagnositcData()
		else:
			print('指令错误\n')
			
			getCMD()
			pass
		with open('driverlist.csv','w',newline='') as f:
			w = None
			count = 0
			for d in data:
				if count == 0:
					w = csv.DictWriter(f,d.keys())
					w.writeheader()
					w.writerow(d)
					count +=1
				else:
					w.writerow(d)
	elif cmd == '11':
		finish_flow_top10 = wd.getTopTen('finish_flow')
		with open('finish_orderTOP10.csv','w',newline='') as f:
			w = csv.DictWriter(f,['序号','姓名','完成流水'])
			w.writeheader()
			count = 1
			for d in finish_flow_top10:
				w.writerow({'序号':str(count),'姓名':d['name'],'完成流水':d['finish_flow']})
				count+=1
		
	elif cmd == '12':
		finish_flow_top10 = wd.getTopTen('serve_score')
		with open('serve_scoreTOP10.csv','w',newline='') as f:
			w = csv.DictWriter(f,['序号','姓名','服务分'])
			w.writeheader()
			count = 1
			for d in finish_flow_top10:
				w.writerow({'序号':str(count),'姓名':d['name'],'服务分':d['serve_score']})
				count+=1
	elif cmd == '13':
		driverlist = wd.getDiagnositcData()
		with open('driver_time_status.csv','w',newline='') as f:
			w = csv.DictWriter(f,['部门','姓名','今日计费时长','目前状态','目前状态时间'])
			w.writeheader()
			for d in driverlist:
				time.sleep(0.1)
				status_r = wd.getResponse('https://wave.xiaojukeji.com/v2/app/order/driverorderlbslist',{'driver_id':d['driver_id']})
				if status_r.json()['errno'] == '0':
					status_time = status_r.json()['data']['monitor']['status_time']
					status = status_r.json()['data']['monitor']['status']
					w.writerow({'部门':d['deparment'],'姓名':d['name'],'今日计费时长':d['charge_time'],'目前状态':status ,'目前状态时间':status_time })
				else:
					print(status_r.json()['error'])
	elif cmd == '14':
		yjb.write_data(yjb.generate_workbook(wd.getYesterday()+'业绩报表'))
	elif cmd == '15':
		url = ''
		payload ={
			"org_id":"",
			"name":"",
			"phone":"",
			"form_type":"1",
			"start_time":wd.getToday(),
			"end_time":wd.getToday(),
			"car_level":"",
			"city":"",
			"order_type":'2',
			"order_column":"",
			"page":'1',
			"size":"100"
		}
		#选择数据分类
		cmd151 = input('请选择数据分类\n1.快车服务业绩\n2.司机投诉\n3.服务评价\n4.完成流水\n>')
		if cmd151 == '1':
			url = 'http://wave.xiaojukeji.com/v2/dc/statisticservescore/driverinfo'
		elif cmd151 == '2':
			url = 'http://wave.xiaojukeji.com/v2/dc/statisticscomplaint/driverinfo'
		elif cmd151 == '3':
			url = 'http://wave.xiaojukeji.com/v2/dc/statisticscomment/driverinfo'
		elif cmd151 == '4':
			url = 'http://wave.xiaojukeji.com/v2/dc/finishorder/driver'
		#选择日期
		cmd152 = input('请填写起始日期\n>')
		cmd153 = input('请填写结束日期\n>')
		payload['start_time'] = cmd152
		payload['end_time'] = cmd153
		
		#选择快车种类
		car_level = input('请选择司机类型(默认快车)\n1.快车\n2.专车\n>')
		if car_level == '1':
			car_level = '500,900'
		elif car_level == '2':
			car_level = '100,200,400'
		payload['car_level'] = car_level
		
		data = wd.getWaveResponse(url,payload)
		
		
		
		with open('totaldata.csv','w',newline='') as f:
			w = None
			count = 0 
			for d in data:
				if count == 0:
					w = csv.DictWriter(f,d.keys())
					w.writeheader()
					w.writerow(d)
					count = 2
				else:
					w.writerow(d)
			
		
		
		
		
getCMD()
	
	
