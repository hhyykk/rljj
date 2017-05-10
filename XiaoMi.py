import requests
import time

millis = int(round(time.time()*1000))

headers={
'Host':'tp.hd.mi.com',
'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
'Accept':'*/*',
'Referer':'http://item.mi.com/product/10000041.html',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
}
cookies = dict(cookies_are='''
xmuuid=XMGUEST-3083A300-F269-11E6-A7F8-BF126F654E0E
__utma=127562001.534333045.1488181125.1488181125.1488181125.1
__utmz=127562001.1488181125.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic

userId=489967425
axmuid=489967425
xm_order_btauth=9ce050ffb12ef7ac255e6374c03c14f6
xm_link_history=EM7MHZb%2FC3CnMZ3jYgUQjNCZPJXX1XQPyjjwZeGhq2M%3D
euid=PriYyffGb%2BxKaCL5cw3iTA%3D%3D
xm_user_www_num=0
XM_489967425_UN=hyk
msttime=http%3A%2F%2Fitem.mi.com%2Fproduct%2F10000041.html
mstz=c063c240876313eb-6492408ebf1654ba|javascript%3Avoid0|353658116.15|pcpid||
mstuid=1487044428223_9055
xm_vistor=1487044428223_9055_1494293441925-1494295069827
log_code=c063c240876313eb-4cd574c9694dd9c9|http%3A%2F%2Fitem.mi.com%2Fproduct%2F10000041.html

''')
url ='http://tp.hd.mi.com/hdinfo/cn'

first_payload = {
	'jsonpcallback':'hdinfo',
	'storage':'422',
	'm':'1',
	'product':'',	
	'source':'',
	'_':millis}
second_payload = {
	'jsonpcallback':'cn2171500039',
	'source':'bigtap',
	'product':'2171500039',
	'addcart':'1',
	'm':'1',
	'fk':''	
	'tsort':'',
	'storage':'422',
	'cstr1':'0',
	'cstr2':'0',
	'r':'',
	'b':'',
	'salt':'51c61358218290c9',
	'ans':'',
	'_':millis,
}

second_payload = {}
r1= requests.get(url,cookies=cookies,headers=headers,params = first_payload)
r2= requests.get(url,cookies=cookies,headers=headers,params = second_payload)
print(r1)
print(r2)