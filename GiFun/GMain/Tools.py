'''小工具（函数）大集合'''

'''========字符处理========'''
## 提取字符串中的汉字 ##
def get_hanzi(str):
	import re
	ns = ['0','1','2','3','4','5','6','7','8','9']
	line = str.strip()  # 处理前进行相关的处理，包括转换成Unicode等
	pattern = re.compile('[^\u4e00-\u9fa50-9]')  # 中文的编码范围是：\u4e00到\u9fa5
	zh = "".join(pattern.split(line)).strip()
	# zh = ",".join(zh.split())
	outStr = zh  # 经过相关处理后得到中文的文本
	zis = []
	
	for j in outStr:
		if j not in ns:
			zis.append(j)
	o = ''.join(zis)
	return o

## 字符串转数字 ##
def word2num(str,c=10):
	import binascii
	string = bytes(str,encoding='utf-8')
	out = int(binascii.hexlify(string),16)
	if c == 8:
		return oct(out)[2:]
	elif c == 16:
		return hex(out)[2:]
	elif c == 2:
		return bin(out)[2:]
	else:
		return out

## 数字转字符串 ##		
def num2word(num):
	import binascii
	num = int(num)
	w = binascii.unhexlify(hex(num)[2:])
	# words = str(w)[2:-1]
	# out = words.encode('raw_unicode_escape').decode()
	out = w.decode()
	return out

## 文本转二维码图片 ##
def make_qr(str,save_path):
	
	import qrcode
	from PIL import Image
	import os
	qr=qrcode.QRCode(
	version=4, #生成二维码尺寸的大小 1-40 1:21*21（21+(n-1)*4）
	error_correction=qrcode.constants.ERROR_CORRECT_M, #L:7% M:15% Q:25% H:30%
	box_size=10, #每个格子的像素大小
	border=2, #边框的格子宽度大小
	)
	qr.add_data(str)
	qr.make(fit=True)
	img=qr.make_image()
	img.save(save_path)
	os.system(save_path)
	
## 生成文本朗读音频文件 ##	
def speech(words):
	from aip import AipSpeech
	from random import randint
	import os
	# 配置百度AI-api
	APP_ID = '15836817'
	API_KEY = 'Yw0nM6YReM6DNHndO4c5qn81'
	SECRET_KEY = 'fVAeZsQaGpbEfkGLsVF5SnTipsRmV7rj'
	client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
	
	result  = client.synthesis(words, 'zh', 1, {
		'vol': 8,'per':5,'spd':4
		})
	mp3 = os.getcwd()+'\\data\\' + words + '.mp3'
	# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
	if not isinstance(result, dict):
		try:
			with open(mp3, 'wb') as f:
				f.write(result)		
		except:
			mp3 = os.getcwd()+'\\data\\' + str(randint(10000000,99999999)) + '.mp3'
			with open(mp3, 'wb') as f:
				f.write(result)		
	return mp3

'''========文件处理========'''
## gif拆分为多张png静态图片 ##
def split_gif(path,sp=''):
	# sp参数若自定义，需在结尾加上‘\\’，如 sp='sp\\'
	import os
	from PIL import Image
	def analyseImage(path):
		im = Image.open(path)
		results = {
			'size': im.size,
			'mode': 'full',
		}
		try:
			while True:
				if im.tile:
					tile = im.tile[0]
					update_region = tile[1]
					update_region_dimensions = update_region[2:]
					if update_region_dimensions != im.size:
						results['mode'] = 'partial'
						break
				im.seek(im.tell() + 1)
		except EOFError:
			pass
		return results
	## main ##
	mode = analyseImage(path)['mode']
	im = Image.open(path)
	i = 0
	p = im.getpalette()
	last_frame = im.convert('RGBA')

	try:
		while True:
			print
			"saving %s (%s) frame %d, %s %s" % (path, mode, i, im.size, im.tile)
			'''
			如果GIF使用本地颜色表，每个框架都有自己的调色板。
			如果没有，我们需要将全局调色板应用到新框架上。
			'''
			if not im.getpalette():
				im.putpalette(p)
			new_frame = Image.new('RGBA', im.size)
			'''
			这个文件是一个“部分”模式的GIF，其中帧更新一个不同大小的区域到整个图像?
			如果是这样，我们需要通过将新框架粘贴到前面的框架上来构建新框架。
			'''
			if mode == 'partial':
				new_frame.paste(last_frame)
			new_frame.paste(im, (0, 0), im.convert('RGBA'))
			#存储到gif所在目录
			spath = '\\'.join(path.split('\\')[:-1])+'\\'+sp+''.join(path.split('\\')[-1].split('.')[:-1])
			new_frame.save('%s-%d.png' % (spath, i), 'PNG')

			i += 1
			last_frame = new_frame
			im.seek(im.tell() + 1)
	except EOFError:
		pass

## 图片转文本风格 ##
def pic2txt(pic,txt,wh=(0.3,0.3),asciis = "@%#&?*+=-. "):
	import os
	from PIL import Image
	img = Image.open(pic)
	out = img.convert("L")
	w = wh[0]
	h = wh[1]
	width,height = out.size
	out = out.resize((int(width * w),int(height * h)))
	width,height = out.size

	# 
	
	texts = ""
	for row in range(height):
		for col in range(width):
			gray = out.getpixel((col,row))
			texts += asciis[int (gray / 255 *(len(asciis)-1))]
		texts += "\n"
	with open(txt,"w") as file:
		file.write(texts)
		out.close()
		os.system('start '+r'C:\\quickstart\\np.lnk '+txt)

## 按像素剪裁图片 ##
def cut_img(img,edth=-24,edtw=0):	
	import cv2
	import os
	# svimg = os.getcwd()+'\\data\\'+img.split('\\')[-1]
	svimg = 'D:\\#My\\GiData\\Source\\arts\\images\\Pics\\TAGL\\cash\\cut\\'+img.split('\\')[-1]
	img = cv2.imread(img)
	h = img.shape[0]
	w = img.shape[1]
	cropped = img[0:h+edth, 0:w+edtw]  # 裁剪坐标为[y0:y1, x0:x1]
	cv2.imwrite(svimg, cropped)

## Matplotlib绘制图表 ##
def draw_f():
	import matplotlib.pyplot as plt	#常用的功能都包含在matplotlib的pyplot方法里面
	import numpy as np
	x = np.linspace(-10000,10000,1000)

	#定义函数(集)
	#-----------------#
	ylist = [
		[3*x**3,'red',2.0,'-'],
		# [22*x+4,'grey',1.0,'-'],
		# [x**2,'blue',1.0,':']
		]
	#-----------------#

	plt.figure(num=3,figsize=(8,5))	#它下面的plot显示在这个figure窗口中
	#num：自定义figure的编号，figsize：窗口长宽
	for y in ylist:
		plt.plot(x,y[0],color=y[1],linewidth=y[2],linestyle=y[3])#'--'代表虚线
	plt.show()	#显示图像

'''========小功能========'''

## 根据输入时间倒计时 ##
def timer():
	# 格式：秒.分.时（“.分.时”或“.时”可以省略）
	import datetime
	import time
	import pygame
	def play_music():
			filepath = "D:\\#My\\python_work\\Gina\\sounds\\dudu.mp3"
			pygame.mixer.init()
			# 加载音乐
			pygame.mixer.init(frequency=1550,size=-16,channels=4)
			pygame.mixer.music.load(filepath)
			# pygame.mixer.music.play(start=0.0)
			#播放时长，没有此设置，音乐不会播放，会一次性加载完
			# time.sleep(30)
			# pygame.mixer.music.stop()
			pygame.mixer.music.play()
	def timer_end(s=0,min=0,h=0,d=0):
		# 参数：秒，分，时，天
		# 返回列表[当前时间，计时后时间]（需格式化）
		cur_time = datetime.datetime.now() #获取当前（系统）时间
		goal = cur_time + datetime.timedelta(days=d,hours=h,minutes=min,seconds=s)
		return [cur_time,goal]

	def er(ask):
		splitasklist = ask.split('.')
		sptimes = []
		try:
			for i in splitasklist:
				sptimes.append(int(i))
			if len(sptimes)==1:
				goallist = timer_end(sptimes[0])
			elif len(sptimes)==2:
				goallist = timer_end(sptimes[0],sptimes[1])
			elif len(sptimes)==3:
				goallist = timer_end(sptimes[0],sptimes[1],sptimes[2])
			elif len(sptimes)==4:
				goallist = timer_end(sptimes[0],sptimes[1],sptimes[2],sptimes[3])
			i_time = datetime.datetime.strftime(goallist[0],'%Y-%m-%d %H:%M:%S')
			o_time = datetime.datetime.strftime(goallist[1],'%Y-%m-%d %H:%M:%S')
			print('*'*50)
			print('开始计时，计时将在',o_time,'结束。')
			print('*'*50)
			print('\n\t\t _ _\\_ _ _/_ _\n\t\t||           ||')
			return goallist[1]
		except:
			print('咦？咦咦咦咦？')
			return datetime.datetime.now()
	def monitorkey(key):
		if keyboard.wait(key):
			return True
	#=========TEST=========
	ask = input('计时时间：')
	def counter(ask):
		while True:
			end = 1
			switch = 0
			goaltime = er(ask)
			while end != '0:00:00':
				showrestdate = goaltime - datetime.datetime.now()
				show = str(showrestdate).split('.')[0]
				print('\r\t\t||__'+show+'__||',end='')
				secondtxt = str(showrestdate).split(':')[-1].split('.')[0]
				end = show
			
			play_music()
			ask = input('\n\n\n\n计时时间：')
	counter(ask)




'''==========Test========='''
# picpath = 'D:\\#My\\GiData\\Source\\Arts\\Images\\Pics\\anqr.liu.iahx.i.hvjp.iyr.o_s.1834.jpg'
# picpath = 'C:\\Users\\111\\Documents\\桌面文件\\(1).jpg'
# pic2txt(picpath,
	# "C:\\Users\\111\\Documents\\桌面文件\\PIC.txt",
	# asciis = "@%#&?*+=-. ",wh=(0.2,0.1))
	
s = bin(877523)
print(s)