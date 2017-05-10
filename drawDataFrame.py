from PIL import Image,ImageFont,ImageDraw
from pandas import DataFrame
from datetime import datetime

def drawDataFrame(frame,filename=datetime.now().strftime('20%y-%m-%d%H:%M:%S.jpg')):
	font = ImageFont.truetype('MSYH.TTC',30)
	im = Image.new('RGB',(1000,100),(0,0,0))
	draw = ImageDraw.Draw(im)
	draw.text((0,0),str(frame.columns),font=font)
	im.save('hello.jpg','JPEG')
	