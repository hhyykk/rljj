#coding:utf-8
import xlsxwriter
import math
import wave
from wave import WaveData as wd
from pandas import Series
ORG_ID_GROUP = (51451,51455,51457,51459,58069,51397,51399,51401,58083,51405,58085)
ORG_ADDRESS = ((2,1),(2,5),(2,9),(2,13),(2,17),(16,1),(16,5),(16,9),(16,13),(16,17),(30,1))
ORG_NAME = (
'仁林1队',
'仁林2队',
'仁林3队',
'仁林4队',
'仁林5队',
'锦江1队',
'锦江2队',
'锦江3队',
'锦江4队',
'锦江5队',
'仁林锦江01队',
)
ORG_CAPTAIN={
	'仁林1队':'袁豪',
	'仁林2队':'李兴',
	'仁林3队':'朱世武',
	'仁林4队':'黎志华',
	'仁林5队':'章亮亮',
	'锦江1队':'邹罚生',
	'锦江2队':'',
	'锦江3队':'',
	'锦江4队':'李俊峰',
	'锦江5队':'何卫喜',
	'仁林锦江01队':'————'
	}


def get_abc_number(abc):
	count = 0
	for a in ABC:
		if a == abc:
			return count
		else:
			count+=1
			continue
def generate_workbook(WBName):
	workbook = xlsxwriter.Workbook(WBName+'.xlsx')
	return workbook
	
class Org:
	def __init__(self,name,drivers,captain,red_per,A_per):
		self.name = name
		self.drivers = drivers
		self.red_per = red_per
		self.A_per =A_per
		
		
def write_data(workbook):	
	org_info_dict = {}
	print('正在初始化。。。')
	#司机总列表
	DriverList = wd.getDiagnositcData(payload={'order_column':'serve_level','order_type':'2'})
	#统计报表里的快车服务业绩
	org_info_r = wd.getResponse('http://wave.xiaojukeji.com/v2/dc/statisticservescore/orginfo',
		{
			'end_time':wd.getYesterday(),
			'form_type':'1',
			'order_type':'2',
			'page':'1',
			'parent_org_id':'4367',
			'size':'30',
			'start_time':wd.getYesterday()
		})
	org_info_data = org_info_r.json()['data']['data']
	for org in org_info_data:
		org_info_dict[org['org_name']] = org
	#公司整体信息	
	OrgDataInfo_r = wd.getResponse('http://wave.xiaojukeji.com/v2/dc/driversurvey/orgdatainfo',{'end_time':wd.getYesterday(),'start_time':wd.getYesterday()})
	OrgDataInfo = OrgDataInfo_r.json()['data']
	def get_format(format_name):
		if format_name=='title':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(20)
			format.set_font_color('black')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_bold(True)
			format.set_border(1)
			format.set_border_color('black')
			return format
		elif format_name == 'sub_title':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(11)
			format.set_font_color('black')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_border(1)
			format.set_border_color('black')
			return format
		elif format_name == 'org_title':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(16)
			format.set_font_color('black')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_pattern(1)
			format.set_bg_color('#FB9966')
			format.set_border(1)
			format.set_border_color('black')
			return format
		elif format_name == 'column':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(10)
			format.set_font_color('black')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_pattern(1)
			format.set_bg_color('#FB9966')
			format.set_border(1)
			format.set_border_color('black')
			return format
		elif format_name == 'unred_body':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(10)
			format.set_font_color('black')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_border(1)
			format.set_border_color('black')
			return format
		elif format_name == 'order_number':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(10)
			format.set_font_color('black')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_pattern(1)
			format.set_bg_color('#FB9966')
			format.set_border(1)
			format.set_border_color('black')
			return format
		elif format_name == 'red_body':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(10)
			format.set_font_color('red')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_border(1)
			format.set_border_color('black')
			return format
		elif format_name == 'bottom':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(10)
			format.set_font_color('red')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_bg_color('yellow')
			format.set_border(1)
			format.set_border_color('black')
			return format
		elif format_name == 'red_captain':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(10)
			format.set_font_color('red')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_bg_color('yellow')
			format.set_border(1)
			format.set_border_color('black')
			return format
		elif format_name == 'unred_captain':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(10)
			format.set_font_color('black')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_bg_color('yellow')
			format.set_border(1)
			format.set_border_color('black')
			return format
		elif format_name == 'common':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(10)
			format.set_font_color('black')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_border(1)
			format.set_border_color('black')
			return format
		elif format_name == 'sched_column_black_green':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(12)
			format.set_font_color('black')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_bg_color('#A8D8B9')
			format.set_border(1)
			format.set_border_color('black')
			format.set_bold(True)
			return format
		elif format_name == 'sched_column_red_green':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(12)
			format.set_font_color('red')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_bg_color('#A8D8B9')
			format.set_border(1)
			format.set_border_color('black')
			format.set_bold(True)
			return format
		elif format_name == 'sched_column_black_yellow':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(12)
			format.set_font_color('black')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_bg_color('yellow')
			format.set_bold(True)
			format.set_border(1)
			format.set_border_color('black')
			return format
		elif format_name == 'sched_column_red_yellow':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(12)
			format.set_font_color('red')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_bg_color('yellow')
			format.set_bold(True)
			format.set_border(1)
			format.set_border_color('black')
			return format
		elif format_name == 'sched_common_black':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(12)
			format.set_font_color('black')
			format.set_align('center')
			format.set_align('vcenter')
			return format
		elif format_name == 'sched_common_red':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(12)
			format.set_font_color('red')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_border(1)
			format.set_border_color('black')
			return format
		elif format_name == 'score_black_yellow':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(12)
			format.set_font_color('black')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_bg_color('yellow')
			format.set_bold(True)
			format.set_border(1)
			format.set_border_color('black')
			return format
		elif format_name == 'red':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(10)
			format.set_font_color('red')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_border(1)
			format.set_border_color('black')
			return format
		elif format_name == 'blue':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(10)
			format.set_font_color('blue')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_border(1)
			format.set_border_color('black')
			return format
		elif format_name == 'green':
			format = workbook.add_format()
			format.set_font_name('微软雅黑')
			format.set_font_size(10)
			format.set_font_color('green')
			format.set_align('center')
			format.set_align('vcenter')
			format.set_border(1)
			format.set_border_color('black')
			return format
	#进度榜
	def writeSchedTable():
		worksheet = workbook.add_worksheet('进度榜')
		worksheet.set_row(0,50)
		
		worksheet.set_column(1,121)
		worksheet.set_column(2,97)
		worksheet.set_column(3,94)
		for i in range(3,12):
			worksheet.set_column(i,94)
		worksheet.merge_range(0,0,0,11,'仁林锦江快车司机目标达成进度表',get_format('title'))
		worksheet.merge_range('I2:L2','数据更新：%s'%wd.getYesterday(),get_format('sched_common_red'))
		worksheet.merge_range(2,0,3,0,'序号',get_format('sched_column_black_green'))
		worksheet.merge_range(2,1,3,1,'队名',get_format('sched_column_black_green'))
		worksheet.merge_range(2,2,3,2,'队长',get_format('sched_column_black_green'))
		worksheet.merge_range(2,3,3,3,'司机人数',get_format('sched_column_black_green'))
		worksheet.merge_range(2,4,2,7,'整体入围率',get_format('sched_column_black_yellow'))
		worksheet.write(3,4,'目标',get_format('sched_column_black_yellow'))
		worksheet.write(3,5,'达成率',get_format('sched_column_red_yellow'))
		worksheet.write(3,6,'达成人数',get_format('sched_column_red_yellow'))
		worksheet.write(3,7,'差距',get_format('sched_column_black_yellow'))
		worksheet.merge_range(2,8,2,11,'整体入围率',get_format('sched_column_black_yellow'))
		worksheet.write(3,8,'目标',get_format('sched_column_black_yellow'))
		worksheet.write(3,9,'达成率',get_format('sched_column_red_yellow'))
		worksheet.write(3,10,'达成人数',get_format('sched_column_red_yellow'))
		worksheet.write(3,11,'差距',get_format('sched_column_black_yellow'))
		
		
		
		MAX = 12
		for i in range(1,MAX):
			worksheet.write(i+3,0,i,get_format('sched_common_black'))
			worksheet.write(i+3,1,ORG_NAME[i-1],get_format('sched_common_black'))
			worksheet.write(i+3,2,ORG_CAPTAIN[ORG_NAME[i-1]],get_format('sched_common_black'))
			worksheet.write(i+3,3,org_info_dict[ORG_NAME[i-1]]['driver_count'],get_format('sched_common_black'))
			worksheet.write(i+3,4,'90%',get_format('sched_common_black'))
			worksheet.write(i+3,5,org_info_dict[ORG_NAME[i-1]]['quality_percent'],get_format('sched_common_black'))
			worksheet.write(i+3,6,org_info_dict[ORG_NAME[i-1]]['quality_count'],get_format('sched_common_black'))
			worksheet.write(i+3,7,math.ceil(0.9*int(org_info_dict[ORG_NAME[i-1]]['driver_count']))-int(org_info_dict[ORG_NAME[i-1]]['quality_count']),get_format('sched_common_black'))
			worksheet.write(i+3,8,'60%',get_format('sched_common_black'))
			worksheet.write(i+3,9,org_info_dict[ORG_NAME[i-1]]['a_level_percent'],get_format('sched_common_black'))
			worksheet.write(i+3,10,org_info_dict[ORG_NAME[i-1]]['a_level'],get_format('sched_common_black'))
			worksheet.write(i+3,11,math.ceil(0.6*int(org_info_dict[ORG_NAME[i-1]]['driver_count']))-int(org_info_dict[ORG_NAME[i-1]]['a_level']),get_format('sched_common_black'))
		Max = MAX
		worksheet.merge_range(Max+3,0,Max+3,1,'合计',get_format('sched_column_red_green'))
		worksheet.write(Max+3,2,'仁林锦江',get_format('sched_column_red_green'))
		
		worksheet.write(Max+3,3,OrgDataInfo['total'],get_format('sched_column_red_green'))
		worksheet.write(Max+3,4,'90%',get_format('sched_column_red_yellow'))
		worksheet.write(Max+3,5,OrgDataInfo['standard_rate'],get_format('sched_column_red_yellow'))
		print(OrgDataInfo)
		worksheet.write(Max+3,6,OrgDataInfo['standard_num'],get_format('sched_column_red_yellow'))
		worksheet.write(Max+3,7,math.ceil(0.9*int(OrgDataInfo['total']))-int(OrgDataInfo['standard_num']),get_format('sched_column_black_yellow'))
		worksheet.write(Max+3,8,'60%',get_format('sched_column_black_yellow'))
		worksheet.write(Max+3,9,OrgDataInfo['level_a_rate'],get_format('sched_column_black_yellow'))
		worksheet.write(Max+3,10,OrgDataInfo['level_a'],get_format('sched_column_black_yellow'))
		worksheet.write(Max+3,11,math.ceil(0.6*int(OrgDataInfo['total']))-int(OrgDataInfo['level_a']),get_format('sched_column_black_yellow'))
	#业绩榜
	def writePerformanceTable():
		worksheet = workbook.add_worksheet('业绩榜')
		def writeOrgData():											
			#业绩榜开始
			worksheet.merge_range('A1:U1','仁林锦江快车业绩榜',get_format('title'))
			A_Min = input('今日A档最低分>\n')
			B_Min = input('今日B档最低分>\n')
			worksheet.merge_range('A2:U2','本月累计计费时长目标：155 小时，当前A档服务分基准线： %s分，B档服务分基准线%s分，当前入围率: %s，A档占比：%s ，数据更新时间：  %s'%(A_Min,B_Min,wd.getCompanyData('入围率'),wd.getCompanyData('A档率'),wd.getYesterday()),get_format('sub_title'))												
			worksheet.set_row(0,37)	
			
			
			worksheet.merge_range(2,0,3,0,'序号',get_format('order_number'))
			worksheet.merge_range(16,0,17,0,'序号',get_format('order_number'))
			worksheet.merge_range(30,0,31,0,'序号',get_format('order_number'))
			worksheet.set_column(0,55)
			total_driver_size = len(DriverList)
			extra_size = int(total_driver_size)-100
			for i in list(range(1,11)):
				worksheet.write(i+3 ,0,i,get_format('common'))
				worksheet.write(i+17,0,i,get_format('common'))
			for i in list(range(1,extra_size)):
				worksheet.write(i+31,0,i,get_format('common'))
			
			def write_org_body(start,org_id):
				org_name_r = wd.getResponse('https://wave.xiaojukeji.com/v2/dc/formfilter/parentorglist',{'org_id':str(org_id)})
				org_name = org_name_r.json()['data']['data'][1]['org_name']
				org_drivers_r = wd.getResponse('https://wave.xiaojukeji.com/v2/dc/driverdiagnosis/driverlist',
				{'end_time':wd.getYesterday(),
				'form_type':'1',
				'order_column':'serve_level',
				'order_type':'2',
				'org_id':str(org_id),
				'page':'1',
				'size':'30',
				'start_time':wd.getYesterday()
				})
				org_drivers = org_drivers_r.json()['data']['data']
				org_captain = ORG_CAPTAIN[org_name]
				
				org_statistic_r = wd.getResponse('https://wave.xiaojukeji.com/v2/dc/statisticservescore/orginfo',
				{
				'end_time':wd.getYesterday(),
				'form_type':'1',
				'order_type':'2',
				'org_id':org_id,
				'page':'1',
				'parent_org_id':'4367',
				'size':'30',
				'start_time':wd.getYesterday()
				})
				org_statistic = org_statistic_r.json()['data']['data'][0]
				
				red_per = org_statistic['quality_percent']
				A_per = org_statistic['a_level_percent']
				
				org = Org(org_name,org_drivers,org_captain,red_per,A_per)
				
				
				driver_counts = len(org_drivers)
				worksheet.merge_range(start[0],start[1],start[0],start[1]+3,org_name,get_format('org_title'))
				worksheet.write(start[0]+1,start[1],'姓名',get_format('column'))
				worksheet.write(start[0]+1,start[1]+1,'计费时长',get_format('column'))
				worksheet.write(start[0]+1,start[1]+2,'服务分',get_format('column'))
				worksheet.write(start[0]+1,start[1]+3,'达成',get_format('column'))
				
				captain = ORG_CAPTAIN[org_name]
				#如果没有队长
				if captain == '' or captain == '————':
					#将各个档次按计费时长排序
					A_team = []
					B_team = []
					C_team = []
					D_team = []
					
					team = []
					
					
					#遍历队伍，找出ABC和未入围司机，并分配到每一组
					for driver  in org_drivers:
						if driver['serve_level'] == 'A':
							A_team.append(driver)
						elif driver['serve_level'] == 'B':
							B_team.append(driver)
						elif driver['serve_level'] == 'C':
							C_team.append(driver)
						elif driver['serve_level'] == '--':
							D_team.append(driver)
					
					A_team = sorted(A_team,key = lambda x : float(x['charge_hours']),reverse = True)
					B_team = sorted(B_team,key = lambda x : float(x['charge_hours']),reverse = True)
					C_team = sorted(C_team,key = lambda x : float(x['charge_hours']),reverse = True)
					D_team = sorted(D_team,key = lambda x : float(x['charge_hours']),reverse = True)
					team +=A_team
					team +=B_team
					team +=C_team
					team +=D_team
				
					for i in range(0,len(team)):
						driver = team[i]
						if driver['serve_level'] != '--':
							worksheet.write(start[0]+2+i,start[1],driver['name'],get_format('red_body'))
							worksheet.write(start[0]+2+i,start[1]+1,driver['charge_hours'],get_format('red_body'))
							worksheet.write(start[0]+2+i,start[1]+2,driver['serve_score'],get_format('red_body'))
							worksheet.write(start[0]+2+i,start[1]+3,driver['serve_level'],get_format('red_body'))
						else:
							worksheet.write(start[0]+2+i,start[1],driver['name'],get_format('unred_body'))
							worksheet.write(start[0]+2+i,start[1]+1,driver['charge_hours'],get_format('unred_body'))
							worksheet.write(start[0]+2+i,start[1]+2,driver['serve_score'],get_format('unred_body'))
							worksheet.write(start[0]+2+i,start[1]+3,driver['serve_level'],get_format('unred_body'))
				#如果有队长
				else:
					#先找出队长，把队长放在第一排
					for driver in org_drivers:
						if driver['name'] == captain:
							if driver['serve_level'] != '--':
								worksheet.write(start[0]+2,start[1],driver['name'],get_format('red_captain'))
								worksheet.write(start[0]+2,start[1]+1,driver['charge_hours'],get_format('red_captain'))
								worksheet.write(start[0]+2,start[1]+2,driver['serve_score'],get_format('red_captain'))
								worksheet.write(start[0]+2,start[1]+3,driver['serve_level'],get_format('red_captain'))
							else:
								worksheet.write(start[0]+2,start[1],driver['name'],get_format('unred_captain'))
								worksheet.write(start[0]+2,start[1]+1,driver['charge_hours'],get_format('unred_captain'))
								worksheet.write(start[0]+2,start[1]+2,driver['serve_score'],get_format('unred_captain'))
								worksheet.write(start[0]+2,start[1]+3,driver['serve_level'],get_format('unred_captain'))
							break
						else:
							continue
					#将各个档次按计费时长排序
					A_team = []
					B_team = []
					C_team = []
					D_team = []
					
					team = []
					
					
					#遍历队伍，找出ABC和未入围司机，并分配到每一组
					for driver  in org_drivers:
						if driver['serve_level'] == 'A':
							A_team.append(driver)
						elif driver['serve_level'] == 'B':
							B_team.append(driver)
						elif driver['serve_level'] == 'C':
							C_team.append(driver)
						elif driver['serve_level'] == '--':
							D_team.append(driver)
					
					A_team = sorted(A_team,key = lambda x : float(x['charge_hours']),reverse = True)
					B_team = sorted(B_team,key = lambda x : float(x['charge_hours']),reverse = True)
					C_team = sorted(C_team,key = lambda x : float(x['charge_hours']),reverse = True)
					D_team = sorted(D_team,key = lambda x : float(x['charge_hours']),reverse = True)
					team +=A_team
					team +=B_team
					team +=C_team
					team +=D_team
					
							
					for i in range(len(team)):
						driver = team[i]
						if driver['serve_level'] != '--':
							worksheet.write(start[0]+3+i,start[1],driver['name'],get_format('red_body'))
							worksheet.write(start[0]+3+i,start[1]+1,driver['charge_hours'],get_format('red_body'))
							worksheet.write(start[0]+3+i,start[1]+2,driver['serve_score'],get_format('red_body'))
							worksheet.write(start[0]+3+i,start[1]+3,driver['serve_level'],get_format('red_body'))
						else:
							worksheet.write(start[0]+3+i,start[1],driver['name'],get_format('unred_body'))
							worksheet.write(start[0]+3+i,start[1]+1,driver['charge_hours'],get_format('unred_body'))
							worksheet.write(start[0]+3+i,start[1]+2,driver['serve_score'],get_format('unred_body'))
							worksheet.write(start[0]+3+i,start[1]+3,driver['serve_level'],get_format('unred_body'))
					
					
				if start[1] == 1:
					worksheet.merge_range(start[0]+driver_counts+2,0,start[0]+driver_counts+3,start[1],'合计',get_format('bottom'))
				else:
					worksheet.merge_range(start[0]+driver_counts+2,start[1],start[0]+driver_counts+3,start[1],'合计',get_format('bottom'))
				worksheet.write(start[0]+driver_counts+2,start[1]+1,'入围率',get_format('bottom'))
				worksheet.write(start[0]+driver_counts+3,start[1]+1,'A档率',get_format('bottom'))
				worksheet.merge_range(start[0]+driver_counts+2,start[1]+2,start[0]+driver_counts+2,start[1]+3,red_per,get_format('bottom'))
				worksheet.merge_range(start[0]+driver_counts+3,start[1]+2,start[0]+driver_counts+3,start[1]+3,A_per,get_format('bottom'))
				
				
				
			#遍历部门ID数组，写入表格中
			for i in list(range(0,len(ORG_ID_GROUP))):
				write_org_body(ORG_ADDRESS[i],ORG_ID_GROUP[i])
		def writeTotal():	
			#部门排行
			Org_Rank_start=(31,7)
			#部门排行初始位置
			ors = Org_Rank_start
			
			worksheet.merge_range(Org_Rank_start[0],Org_Rank_start[1],Org_Rank_start[0],Org_Rank_start[1]+7,"团队排名",get_format('score_black_yellow'))
			worksheet.merge_range(ors[0]+1,ors[1],ors[0]+1,ors[1]+1		,'车队',get_format('score_black_yellow'))
			worksheet.write(      ors[0]+1,ors[1]+2				   		,'队长',get_format('score_black_yellow'))
			worksheet.write(      ors[0]+1,ors[1]+3				   		,'入围率',get_format('score_black_yellow'))
			worksheet.write(      ors[0]+1,ors[1]+4				   		,'排名',get_format('score_black_yellow'))
			worksheet.merge_range(ors[0]+1,ors[1]+5				   		,ors[0]+1,ors[1]+6,'A档占比',get_format('score_black_yellow'))
			worksheet.write(      ors[0]+1,ors[1]+7				   		,'排名',get_format('score_black_yellow'))
			worksheet.merge_range(ors[0]+12,ors[1],ors[0]+12,ors[1]+2	,'合计',get_format('sched_column_red_yellow'))
			worksheet.write(      ors[0]+12,ors[1]+3					,OrgDataInfo['standard_rate'],get_format('sched_column_red_yellow'))
			worksheet.write(      ors[0]+12,ors[1]+4					,'————',get_format('sched_column_red_yellow'))
			worksheet.merge_range(ors[0]+12,ors[1]+5,ors[0]+12,ors[1]+6 ,OrgDataInfo['level_a_rate'],get_format('sched_column_red_yellow'))
			worksheet.write(      ors[0]+12,ors[1]+7					,'————',get_format('sched_column_red_yellow'))
			for i in range(10):
				worksheet.merge_range(ors[0]+2+i,ors[1],ors[0]+2+i,ors[1]+1,ORG_NAME[i],get_format('common'))
				worksheet.write(ors[0]+2+i,ors[1]+2,ORG_CAPTAIN[ORG_NAME[i]],get_format('common'))
				worksheet.write(ors[0]+2+i,ors[1]+3,org_info_dict[ORG_NAME[i]]['quality_percent'],get_format('common'))
				worksheet.merge_range(ors[0]+2+i,ors[1]+5,ors[0]+2+i,ors[1]+6,org_info_dict[ORG_NAME[i]]['a_level_percent'],get_format('common'))

		writeOrgData()
		writeTotal()
	#日报表
	def writeDailyTable():
		worksheet = workbook.add_worksheet('日报表')
		columns = ['序号','司机','司机手机号','是否达标','档位','服务分','累计计费时长(小时)','当日计费时长(小时)']
		for i in range(len(columns)):
			worksheet.write(0,i,columns[i],get_format('sched_column_black_yellow'))
			worksheet.set_column(i,150)
		#遍历司机列表写入日报表中
		for i in range(len(DriverList)):

			format = None
			d = DriverList[i]
			IsRed = ''
			if d['serve_level'] == '--':
				IsRed = '否'
			else:
				IsRed = '是'
			if d['serve_level'] == 'A':
				format = get_format('red')
			elif d['serve_level'] == 'B':
				format = get_format('blue')
			elif d['serve_level'] == 'C':
				format = get_format('green')
			elif d['serve_level'] == '--':
				format = get_format('common')
			worksheet.write(i+1,0,i+1,format)
			worksheet.write(i+1,1,d['name'],format)
			worksheet.write(i+1,2,d['phone'],format)
			worksheet.write(i+1,3,IsRed,format)
			worksheet.write(i+1,4,d['serve_level'],format)
			worksheet.write(i+1,5,d['charge_hours'],format)
			worksheet.write(i+1,6,d['redline_charge_time'],format)
			worksheet.write(i+1,7,d['charge_time'],format)
					
	#计费时长表
	def writeTimeTable():
		ws = workbook.add_worksheet('计费时长')
		columns = ['序号','司机','档位','累计计费时长(小时)','红线时长(小时)','当日计费时长(小时)']
		#写标题
		for i in range(len(columns)):
			ws.write(0,i,columns[i],get_format('sched_column_red_yellow'))
			ws.set_column(i,150)
		TOP =10
		count = 0
		driverlist = wd.getDiagnositcData(payload = {'order_column':'charge_hours','order_type':'2'})
		for i in range(len(driverlist)):
			d = driverlist[i]
			format = None
			if i < TOP:
				format = get_format('red')
			else:
				format = get_format('common')
			ws.write(i+1,0,i+1,format)
			ws.write(i+1,1,d['name'],format)
			ws.write(i+1,2,d['serve_level'],format)
			ws.write(i+1,3,d['charge_hours'],format)
			ws.write(i+1,4,d['redline_charge_time'],format)
			ws.write(i+1,5,d['charge_time'],format)
			
	#服务分表
	def writeScoreTable():
		ws = workbook.add_worksheet('服务分')
		driverlist = wd.getDiagnositcData(payload={'order_column':'serve_score'})
		columns = ['序号','司机','档位','服务分']
		for i in range(len(columns)):
			ws.write(0,i,columns[i],get_format('sched_column_red_yellow'))
			ws.set_column(i,150)
		for i in range(len(driverlist)):
			d = driverlist[i]
			format = None
			if i <10:
				format = get_format('red')
			else:
				format = get_format('common')
			ws.write(i+1,0,i+1,format)
			ws.write(i+1,1,d['name'],format)
			ws.write(i+1,2,d['serve_level'],format)
			ws.write(i+1,3,d['serve_score'],format)
			
	#流水表
	def writeFlowTable():
		ws = workbook.add_worksheet('流水')
		driverlist = wd.getWaveResponse('http://wave.xiaojukeji.com/v2/dc/finishorder/driver',{
		'car_level':'500,900',
		'end_time':wd.getYesterday(),
		'form_type':'1',
		'order_column':'finish_flowfee',
		'order_type':'2',
		'size':'100',
		'start_time':wd.getYesterday(),
		})
		columns =['序号','司机姓名','流水金额(元)','完成单量','在线时长(小时)','服务时长(小时)','车里程(公里)','单里程(公里)']
		
		for i in range(len(columns)):
			ws.write(0,i,columns[i],get_format('sched_column_red_yellow'))
			ws.set_column(i,150)
		for i in range(len(driverlist)):
			format = None
			if i <10:
				format = get_format('red')
			else:
				format = get_format('common')
			d = driverlist[i]
			ws.write(i+1,0,i+1,format)
			ws.write(i+1,1,d['name'],format)
			ws.write(i+1,2,d['finish_flowfee'],format)
			ws.write(i+1,3,d['finish_finish_cnt'],format)
			ws.write(i+1,4,d['finish_online_time'],format)
			ws.write(i+1,5,d['finish_serve_time'],format)
			ws.write(i+1,6,d['finish_work_distance'],format)
			ws.write(i+1,7,d['finish_serve_distance'],format)
	
	#好评表
	def write5StarTable():
		worksheet = workbook.add_worksheet('好评')
		columns = ['姓名','队伍','接单时间','星级','评价内容']
		for i in range(len(columns)):
			worksheet.write(0,i,columns[i],get_format('sched_column_black_yellow'))
			worksheet.set_column(i,151)

		text_orders_group = wd.getCompanyData('文字好评',params_plus={'star':'5','start_time':wd.getYesterday(),'end_time':wd.getYesterday()})
		for i in range(len(text_orders_group)):
			order = text_orders_group[i]
			worksheet.write(i+1,0,order['name'],get_format('common'))
			worksheet.write(i+1,1,order['org_route'],get_format('common'))
			worksheet.write(i+1,2,order['strived_time'],get_format('common'))
			worksheet.write(i+1,3,order['star'],get_format('common'))
			try:
				worksheet.write(i+1,4,order['comment'],get_format('common'))
			except Exception as e:
				worksheet.write(i+1,4,'null',get_format('common'))
		
	#差评表
	def writeLowStarTable():
		worksheet = workbook.add_worksheet('差评')
		columns = ['姓名','队伍','接单时间','星级','评价内容']
		for i in range(len(columns)):
			worksheet.write(0,i,columns[i],get_format('sched_column_black_yellow'))
			worksheet.set_column(i,151)

		text_orders_group = wd.getCompanyData('文字好评',params_plus={'star':'1,2,3','start_time':wd.getYesterday(),'end_time':wd.getYesterday()})
		for i in range(len(text_orders_group)):
			order = text_orders_group[i]
			worksheet.write(i+1,0,order['name'],get_format('common'))
			worksheet.write(i+1,1,order['org_route'],get_format('common'))
			worksheet.write(i+1,2,order['strived_time'],get_format('common'))
			worksheet.write(i+1,3,order['star'],get_format('common'))
			try:
				worksheet.write(i+1,4,order['comment'],get_format('common'))
			except Exception as e:
				worksheet.write(i+1,4,'null',get_format('common'))



	#投诉表
	def writeComplaintTable():
		worksheet = workbook.add_worksheet('投诉')
		columns = ['姓名','队伍','接单时间','投诉分类','投诉内容']
		for i in range(len(columns)):
			worksheet.write(0,i,columns[i],get_format('sched_column_black_yellow'))
			worksheet.set_column(i,151)

		complaint_group = wd.getCompanyData('投诉',params_plus={'start_time':wd.getYesterday(),'end_time':wd.getYesterday()})
		for i in range(len(complaint_group)):
			order = complaint_group[i]
			worksheet.write(i+1,0,order['name'],get_format('common'))
			worksheet.write(i+1,1,order['org_name'],get_format('common'))
			worksheet.write(i+1,2,order['strived_time'],get_format('common'))
			worksheet.write(i+1,3,order['complaint_type'],get_format('common'))
			try:
				worksheet.write(i+1,4,order['complaint_info'],get_format('common'))
			except Exception as e:
				worksheet.write(i+1,4,'null',get_format('common'))





	
	writeSchedTable()
	writePerformanceTable()
	writeDailyTable()
	writeTimeTable()
	writeScoreTable()
	writeFlowTable()
	write5StarTable()
	writeLowStarTable()
	writeComplaintTable()
	
	#关闭文件流，不写这条会出错
	workbook.close()
	
