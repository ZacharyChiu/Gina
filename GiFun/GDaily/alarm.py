'''时间管理模块'''
'''
目标
实现计时功能
实现闹钟
'''
import datetime
import time
import pygame
def play_music():
		filepath = "D:\\#My\\python_work\\Gina\\sounds\\dudu.mp3"
		pygame.mixer.init()
		# 加载音乐
		pygame.mixer.init(frequency=1550,size=-16,channels=4)
		pygame.mixer.music.load(filepath)
		pygame.mixer.music.play()



def timer_end(s=0,min=0,h=0,d=0):
	# 参数：秒，分，时，天
	# 返回列表[当前时间，计时后时间]（需格式化）
	cur_time = datetime.datetime.now() #获取当前（系统）时间
	goal = cur_time + datetime.timedelta(days=d,hours=h,minutes=min,seconds=s)
	return [cur_time,goal]

def timer(ask):
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
		print('倒计时',o_time,'结束。') 
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
		goaltime = timer(ask)
		while end != 0:
			showrestdate = goaltime - datetime.datetime.now()
			print('\r\t\t||__'+str(showrestdate).split('.')[0]+'__||',end='')
			secondtxt = str(showrestdate).split(':')[-1].split('.')[0]
			end = int(secondtxt)
		
		play_music()
		ask = input('\n\n\n\n计时时间：')
		

counter(ask)


