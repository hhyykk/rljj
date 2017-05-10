import requests
import datetime
import time
from calendar import monthrange
import itchat
import wave
from PIL import Image,ImageFont,ImageDraw
itchat.auto_login()
chatRooms = itchat.get_chatrooms(update=True)
nickNames=['锦江一队','锦江二队','锦江三队','锦江四队','锦江五队','仁林一队','仁林二队','仁林三队','仁林四队']
org_ids=[51397,			51399,		51401,		51403,		51405,		51451,51455,		51457,	51459]

#快车司机诊断地址
url="http://wave.xiaojukeji.com/v2/dc/driverdiagnosis/driverlist"
#完成流水地址
FinishOrderUrl='http://wave.xiaojukeji.com/v2/dc/finishorder/driver'
FileCookie=open('WaveCookie.txt','r').read()
cookie=dict(cookies_are=FileCookie)
header={
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
'Accept':'application/json, text/javascript, */*; q=0.01',
'Connection':'keep-alive',
'Host':'wave.xiaojukeji.com',
'Referer':'https://wave.xiaojukeji.com/v2/'
}
stime = datetime.datetime.now().strftime('20%y-%m-%d')
size='100'




def sendOrgMessage():
	for chatRoom in chatRooms:
		for i in range(len(nickNames)):
			if nickNames[i] == chatRoom['NickName']:
				fileDir = drawList(getDriverList(org_ids[i]),org_ids[i],nickNames[i])
				print(itchat.send_image(fileDir,chatRoom['UserName']))

def getDriverList(OrgId):
	OrgId = str(OrgId)
	FileCookie=open('WaveCookie.txt','r').read()
	cookie=dict(cookies_are=FileCookie)
	header={
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	'Accept':'application/json, text/javascript, */*; q=0.01',
	'Connection':'keep-alive',
	'Host':'wave.xiaojukeji.com',
	'Referer':'https://wave.xiaojukeji.com/v2/'
	}
	stime = datetime.datetime.now().strftime('20%y-%m-%d')
	size='100'
	model='5'
	param = {'start_time':stime,'model':model,'size':'100','org_id':OrgId}
	dr = requests.get(url,cookies=cookie,params=param,headers=header)
	#获取全部司机，通过号码来获取司机具体数据
	DriverListData=dr.json()['data']['data']
	return DriverListData
	
def getResponse(url,param):
	return requests.get(url,params=param,cookies=cookie,headers=header)


def getOrgIds():
	PlatformUrl='http://wave.xiaojukeji.com/v2/app/org/orgtree?platform=1'
	r = getResponse(PlatformUrl,{})
	OrgIds = []
	data = r.json()['data']
	for d in data:
		OrgIds.append(d['id'])
	return OrgIds
driverbindlist = {}
def init():
	print('正在初始化..')
	OrgIds = getOrgIds()
	for orgid in OrgIds:
		payload = {'org_id':orgid,'size':'30'}
		r = getResponse('http://wave.xiaojukeji.com/v2/app/orgdriver/driverbindlists',payload)
		errno = r.json()['errno']
		if errno != '0':
			continue
		data = r.json()['data']['data']
		if len(data) != 0:
			print(orgid,len(data))
			for d in data:
				driverbindlist[d['phone']]=d['_create_time']
	print('初始化完毕')

def timeDelta(time):
	delta = (datetime.datetime.now()-datetime.datetime.strptime(time,'20%y-%m-%d %H:%M:%S')).days
	return delta				
#查看司机是否有资格拿奖励 转对公十天以上
def CanReward(phone):
	if phone in driverbindlist:
		time = timeDelta(driverbindlist[phone])
		if time >10:
			return True
		else:
			return False
	else:
		return False
	
def getToday25Delta():
	month_last_day = monthrange(2017,int(datetime.datetime.now().month))[1]
	delta = month_last_day-datetime.datetime.now().day
	return delta


	
def drawList(data,OrgId,name):
	print('正在生成%s的奖励图片' % name)
	width = 1900
	count = len(data)
	length = (1+count)*50
	im = Image.new('RGB',(width,50+length),(255,255,255))
	font = ImageFont.truetype('msyhbd.ttc',38)
	draw = ImageDraw.Draw(im)
	marginTop = 80
	marginLeft = 10
	
	TotalTimeXOffset = 150
	TodayTimeXOffset =380
	LevelXOffset = 650
	RewardXOffset =1050
	DistanceXOffset = 1300
	FinishOrderXOffset = 1600
	
	
	fontTitle=ImageFont.truetype('msyhbd.ttc',45)
	draw.ink=0
	draw.text([marginLeft,10],name,font=fontTitle)
	
	
	draw.ink= 16711680
	
	draw.text([marginLeft,marginTop],'姓名',font=font)
	draw.text([marginLeft + TotalTimeXOffset,marginTop],'服务分',font=font)
	draw.text([marginLeft + TodayTimeXOffset,marginTop],'今日计费时长',font=font)
	draw.text([marginLeft + LevelXOffset,marginTop],'累计计费时长',font=font)
	draw.text([marginLeft + RewardXOffset,marginTop],'距离红线时长',font=font)
	draw.text([marginLeft + DistanceXOffset,marginTop],'今日计划时长',font=font)
	
	
	
	draw.ink=0
	
	cnt = 0
	reward = 0
	
	ACount= 0
	for d in data:
		if d['serve_level'] == 'A':
			ACount += 1
	
	
	
	for d in data:
		time.sleep(0.4)
		cnt+=1
		
		if CanReward(d['phone']) == False:
			reward = '0'
		else:
			if (d['serve_level'] == 'B') & (float(d['serve_score']) >= 84 ):
				reward = '100'
			else:
				if (d['serve_level'] =='A') & (float(d['serve_score']) >=91 ):
					if (ACount >0) & (ACount <= 3):
						reward = '400'
					elif (ACount>=4) & (ACount<=6):
						reward = '500'
		ADeta = str(round(float(d['serve_score'])-91,1))
		RedDeta = round(float(d['total_charge_time'])-float(d['redline_charge_time']),1)
		today_25_delta = getToday25Delta()
		if RedDeta >=0:
			plan_hours='5'
		else:
			plan_hours = str(5-round(RedDeta/today_25_delta,1)+1)
		FinishOrderResponse =wave.getResponse(FinishOrderUrl,{'phone':d['phone']})
		try:
			FinishOrder = FinishOrderResponse.json()['data']['data'][0]['finish_flowfee']
		except Exception as e:
			print(FinishOrderResponse.text)
			print(e)
			FinishOrder = '数据异常'
		draw.text([marginLeft,marginTop+cnt*40],d['name'],font=font)
		draw.text([marginLeft + TotalTimeXOffset,marginTop   + cnt*40],d['serve_score'],font=font)
		draw.text([marginLeft + TodayTimeXOffset,marginTop   + cnt*40],d['charge_time'],font=font)
		draw.text([marginLeft + LevelXOffset,marginTop       + cnt*40],d['total_charge_time'],font=font)
		draw.text([marginLeft + RewardXOffset,marginTop      + cnt*40],str(RedDeta),font=font)
		draw.text([marginLeft + DistanceXOffset,marginTop    + cnt*40],plan_hours,font=font)
		reward = 0
		
		
		
		
		
		
	im.save(str(OrgId)+'.jpg','JPEG')
	return str(OrgId)+'.jpg'


class Org():
	def __init__(self,finish_avg_flowfee,finish_fee_time,finish_finish_cnt,finish_flowfee,finish_online_time,finish_order_driver,finish_serve_distance,finish_serve_time,finish_work_distance,org_id,org_name):	
		self.finish_avg_flowfee      =finish_avg_flowfee
		self.finish_fee_time  		 =finish_fee_time
		self.finish_finish_cnt	     =finish_finish_cnt
		self.finish_flowfee          =finish_flowfee
		self.finish_online_time      =finish_online_time
		self.finish_order_driver     =finish_order_driver
		self.finish_serve_distance   =finish_serve_distance
		self.finish_serve_time       =finish_serve_time
		self.finish_work_distance    =finish_work_distance
		self.org_id                  =org_id
		self.org_name                =org_name
		
def getData():
	r = download()
	Data = MakeObject(r)
	return Data
	
def DrawRank(Arr):
	width = 512
	length = 1024
	bannerLength = 50
	bannerTop = 10
	im = Image.new('RGB',(width,length),'white')
	font = ImageFont.truetype('msyhbd.ttc',24)
	draw = ImageDraw.Draw(im)
	draw.polygon([(0,bannerLength),(width,bannerLength),(width,bannerTop),(0,bannerTop)],fill='#255359')
	#打开奖章文件
	No1Im = Image.open('no1.png')
	No2Im = Image.open('no2.png')
	No3Im = Image.open('no3.png')
	
	
	#将奖章粘贴在画板上
	im.paste(No1Im,[10,bannerLength+bannerTop+10])
	im.paste(No2Im,[10,bannerLength+bannerTop+10+No1Im.size[1]])
	im.paste(No3Im,[10,bannerLength+bannerTop+10+No1Im.size[1]+10+No1Im.size[1]])
	
	#写标题
	draw.ink=16777215
	draw.text([5,12],'深圳市仁林锦江汽车服务有限公司平均流水排名',font = font)
	
	
	Name_Font = ImageFont.truetype('msyhbd.ttc',46)
	print(Arr)
	#冠军写字
	draw.ink=0
	yOffset = 10
	draw.text([270,bannerLength+bannerTop+yOffset+10],'冠军队伍',font=Name_Font)
	draw.text([270,bannerLength+bannerTop+yOffset+60],Arr[0].org_name,font=Name_Font)
	draw.text([270,bannerLength+bannerTop+yOffset+110],Arr[0].finish_avg_flowfee,font=Name_Font)
	
	SecondY = bannerLength+bannerTop+yOffset+120
	
	draw.text([270,SecondY+100+20],'亚军队伍',font=Name_Font)
	draw.text([270,SecondY+150+20],Arr[1].org_name,font=Name_Font)
	draw.text([270,SecondY+200+20],Arr[1].finish_avg_flowfee,font=Name_Font)
	
	ThirdY = SecondY+230
	draw.text([270,ThirdY+100+20],'季军队伍',font=Name_Font)
	draw.text([270,ThirdY+150+20],Arr[2].org_name,font=Name_Font)
	draw.text([270,ThirdY+200+20],Arr[2].finish_avg_flowfee,font=Name_Font)
	
	FourThY = ThirdY + 200 + 20 + 100
	count = 0
	Margin = 30
	for i in range(len(Arr)-3):
		draw.text([30,FourThY+i*Margin],str(4+i),font=font)
		draw.text([150,FourThY+i*Margin],Arr[3+i].org_name,font=font)
		draw.text([400,FourThY+i*Margin],Arr[3+i].finish_avg_flowfee,font=font)
	
	
	
	
	im.save('orgrank.jpg','JPEG')
	return 'orgrank.jpg'

def download():
	url = 'https://wave.xiaojukeji.com/v2/dc/finishorder/org'
	payload={'model':'5','parent_org_id':'4367','size':'30','start_time':datetime.datetime.now().strftime('20%y-%m-%d')}
	r = requests.get(url,params=payload,cookies=cookie,headers=header)
	return r
def MakeObject(r):
	data = r.json()['data']['data']
	OrgArr=[]
	for d in data:
		org = Org(d['finish_avg_flowfee'], d['finish_fee_time'],d['finish_finish_cnt'],d['finish_flowfee'],d['finish_online_time'],d['finish_order_driver'],d['finish_serve_distance'],d['finish_serve_time'],d['finish_work_distance'],d['org_id'],d['org_name'])
		OrgArr.append(org)
		
	RankedOrgArr = sorted(OrgArr,key = lambda x:-float(x.finish_avg_flowfee))
	return RankedOrgArr
				
def sendFinishOrderToCoptain():
	for chatroom in chatRooms:
		if chatroom['NickName'] == '仁林锦江:队长群':
			itchat.send_image(DrawRank(getData()),chatroom['UserName'])
			break

