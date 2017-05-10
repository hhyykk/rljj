import requests
import hashlib
import urllib.request
import random

def fanyi(q):
    appid = '20170418000045085'
    secretKey = 'dUubZe55tMitFjjEllX9'
    
    myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    fromLang = 'en'
    toLang = 'zh'
    salt = random.randint(32768, 65536)
    
    sign = appid+q+str(salt)+secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode('utf-8'))
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.request.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    
    try:
        response = requests.get(myurl)
		result =response.json()['trans_result']
		
    except Exception as  e:
        print (e)