# -*- coding = utf-8 -*-
# Author: Zachary
# @Time: 2020/10/4 16:43

import os
import sys
import pyperclip
import random
import time
import datetime
import re
from bs4 import BeautifulSoup
from mutagen.mp3 import MP3
import csv
import logging
from mutagen.mp3 import MP3
# from pydub import AudioSegment

# 自建库
sys.path.append('../GHuman')
from ChatMe import chatme
import Ali_TTS as tts
import ghuman
sys.path.append('../GData')
from Spider import trans_yzdc as trans
from Spider import spider
logging.getLogger("requests").setLevel(logging.WARNING)
os.system('color 70')



with open('D:\#My\GiData\Creation\Projects\Python\Gina\GiFun\GMain\main_config.ini', encoding='utf-8') as f:
	text = f.read()
ini = BeautifulSoup(text, 'html.parser')


def a(tag):
	# 获取配置文件结构树（基于html标签系统）
	try:
		r = eval(tag.string.strip())
	except:
		r = tag.string.strip()
	return r



def kill_biaodian(s):
	# 去掉所有标点
	punc = '~`!#$%^&*()_+-=|\';“”:/.,?><~·！@#￥%……&*（）——+-=“：’；、。，？》《{}'
	return re.sub(r"[%s]+" %punc, "",s)

	
def find_file(pan,filename,mode=''):
	i = 0
	result = []
	open_dic = {'py':'C:\\MySoftware\\Notepad++\\notepad++.exe','txt':'C:\\MySoftware\\Notepad++\\notepad++.exe'}
	if mode == 'full':
		print('严厉搜索...')
	else:
		print('模糊搜索...')
	for root, lists, files in os.walk(pan):
		for file in files:
			if mode == 'full':
				if filename.lower() == file.lower():
					i = i + 1
					write = os.path.join(root, file)
					print('%d %s' % (i, write))
					result.append([root,write])
			else:
				if filename.lower() in file.lower():
					i = i + 1
					write = os.path.join(root, file)
					print('%d %s' % (i, write))
					result.append([root,write])
	asks = input('Open? [op+number / number / any]').split(' ')
	if result:
		try:
			index = int(asks[0])
			os.startfile(result[0])
		except:
			if asks[0] == 'op':
				try:
					index2 = int(asks[1])
					filetype = result[1][index2].split('.')[-1]
					if filetype in open_dic:
						os.system('start ' + open_dic[filetype] + ' ' + result[1][index2])
					else:
						os.system('start ' + result[1][index2])
				except Exception as e:
					print(e)
			elif asks == 'op':
				os.system('start '+result[1])
		else:
			if ask == 'y' or ask == '1':
				os.startfile(result[0])
	

def find_dir(pan,dirname,mode='',showlen=1):
	i = 0
	result = []
	if mode == 'full':
		print('严厉搜索...')
	else:
		print('模糊搜索...')
	for root, lists, files in os.walk(pan):
		for jia in lists:
			if mode == 'full':
				if dirname.lower() == jia.lower():
					i = i + 1
					write = os.path.join(root, jia)
					print('%d %s' % (i, write))
					result.append(write)
			else:
				if dirname.lower() in jia.lower():
					i = i + 1
					write = os.path.join(root, jia)
					s = '\\'.join(write.split('\\')[showlen:])
					print('%d %s' % (i, s))
					result.append(write)
	ask = input('Open? [y/number/any]')
	if result:
		if len(result)>1:
			try:
				index = int(ask)
				os.startfile(result[index-1])
			except:
				if ask == 'y':
					os.startfile(result[0])
				else:
					pass
		else:
			if ask == 'y' or ask == '1':
				os.startfile(result[0])

# def speech.timelog():
	# cur_time = datetime.datetime.now()  # 数据类型为：datetime
	# now = str(cur_time).split('.')[0]
	# date = ''.join(now.split(' ')[0].split('-'))
	# time = ''.join(now.split(' ')[1].split(':'))
	# t = date + time
	# return t


	

		
# 打招呼
speech = ghuman.Speech()
sayhi = {1:'morning',2:'beforenoon',3:'noon',4:'afternoon',5:'night',6:'midnight'}
timenum = speech.timelog()[8:-2]

if int(timenum) in range(400,900):
	timecode = 1
elif int(timenum) in range(900,1130):
	timecode = 2
elif int(timenum) in range(1130,1300):
	timecode = 3
elif int(timenum) in range(1300,1730):
	timecode = 4
elif int(timenum) in range(1730,2330):
	timecode = 5
else:
	timecode = 6

try:
	moji = spider.Moji()
	wea = moji.now
	speech.say('[hi]'+sayhi[timecode])
	speech.say('gina_serving')
	# say(speak('现在天气' + wea[0] + ',' + wea[1] + '℃',name='[Weather]'+speech.timelog()),dir='')
	text = '现在天气' + wea[0] + ',' + wea[1] + '℃'
	os.system('CLS')
	# 检测音库是否已有
	with open('tts_logs\\log_dic.txt','r',encoding='utf-8') as f:
		log_list = f.readlines()
		logname = []
		logcontent = []
		for l in log_list:
			if l[0] != '#':
				aaa = l.split('\t')[0]
				bbb = '\t'.join(l.split('\t')[1:]).strip()
				if bbb not in logcontent:
					logcontent.append(bbb)
					logname.append(aaa)
	if text in logcontent:
		speech.say('tts_logs\\'+logname[logcontent.index(text)],dir='',t='x')
	else:
		log_name = speech.speak(text,name='tts_logs\\[Weather]'+speech.timelog(),dir='',t='x').split('\\')[-1]
		with open('tts_logs\\log_dic.txt','a',encoding='utf-8') as f:
			f.write(log_name+'\t'+text+'\n')
	os.system('CLS')
	print('现在【%s,%s℃】'%(wea[0],wea[1]))
except Exception as e:
	print('获取天气遇到问题。')
	# speech.say('[hi]'+sayhi[timecode])
	# speech.say('gina_serving')
	print(e)






# play_music(a(ini.bgm),16000,'x')

gidata_dic = a(ini.gidata)
web_dic = a(ini.webdic)
order_collection = a(ini.orders)
id = a(ini.id)[0]
id_key = a(ini.id)[1]



# month = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
# 'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
# zimu = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

bs_webs = []
webs = []
for key in web_dic:
	webs.append(key)
# for key in bsweb_dic:
# bs_webs.append(key)
# print(webs)
quick_list = os.listdir('C:\\quickstart')
orders = [[],
		  ['Gina', '姬娜', '小姬姬', '聊天', 'chat'],
		  quick_list
		  ]
cmddic = {'t': 'taskmgr'}
cmdqk = []
for key in cmddic:
	cmdqk.append(key)

ask = ''
# os.system('CLS')  #清屏
while ask != 'quit':
	try:
		Round = 0
		ask = input('$ 控制台：')
		if ask == 're':
			print('\n\n')
			p = os.getcwd()
			c = os.path.basename(__file__)
			# print(p+'\\'+c)
			# say('ok')
			speech.say('restart',t='x')
			os.system('python '+p+'\\'+c)
			print('\n')
			Round = 0
		
		elif ask == 'speak':
			s = input('You Say: ')
			speak(s)
			# say('AAAAAA')
		
		elif ask == 'help':
			for i in quick_list:
				# print(orders[2][i],'->',lnk[i])
				print(i)
			print('\n')
		elif ask == '==':
			inp = input('Calculator: ')
			while inp != 'q':
				result = eval(inp)
				print('Result:',result)
				print('-'*50)
				inp = input('Calculator: ')
		# 运行py程序
		elif ask == 'tag':
			os.system('start python D:\\#My\\GiData\\Creation\\Projects\\Python\\Gina\\GiFun\\GData\\Tags\\Tags_win.py')
			print('\n')
		
		elif ask[:3] == 'ts ':
			r = trans.trans(ask[3:])
			print('>>>',r)
		elif ask == 'cip':
			# color in pic
			os.system('start python D:\\#My\\GiData\\Creation\\Projects\\Python\\Gina\\GiFun\\GShow\\ColorInPic.py')
			print('\n')
		# elif ask == 'dc':
			# # draw color
			# os.system('python D:\\#My\\GiData\\Creation\\Projects\\Python\\Gina\\GiFun\\GData\\Color\\draw_colors.py')
			# print('\n')

		# elif ask in orders[1]:
		# os.system('start python D:/#My/python_work/Gina/ChatWindow_2.0.py')
		# print('\n')
		elif ask == 'fname':
			os.system('python D:/#My/python_work/EditFileName.py')
			print('\n')

		elif ask == 'timer':
			os.system('start python D:\\#My\\python_work\\System\\timer.py')
			print('\n')


		elif ask == '2':
			print('\n\n')
			os.system('start python D:/#My/python_work/System/ToOpen.py')
			print('\n')

		elif ask == 'rmb':
			print('\n\n')
			os.system('python D:/#My/python_work/Data_Technology/Account.py')
			print('\n')

		elif ask == 'cd':
			print('\n\n')
			os.system('python D:/#My/python_work/System/cd.py')
			print('\n')

		elif ask == 'qr':
			os.system('python D:/#My/python_work/pics/make_qr.py')
			print('\n')
		elif ask == 'hand':
			os.system('start python D:/#My/python_work/System/HandControl.py')
			print('\n')

		# 运行cmd命令
		elif ask == 'cmd':
			oo = input('cmd：')
			while oo != 'q':
				os.system(oo)
				oo = input('cmd：')
			print('\n')
		elif ask == 'py3':
			os.system('python')
		elif ask in cmdqk:
			os.system(cmddic[ask])


		# 打开快捷方式
		elif ask == 'ybxl':
			pyperclip.copy('ybxlbiji000080')
			pyperclip.paste()
			pyperclip.copy('1563382991@qq.com')
			os.system(r'start C:\\quickstart\\ybxl.lnk')
			
		elif ask + '.lnk' in quick_list:
			# smallize()
			path = 'start C:/quickstart/' + ask + '.lnk'
			speech.say('oky')
			time.sleep(0.5)
			# say(['opening',ask])
			speech.say('opening')
			try:
				speech.say(ask)
			except:
				print('没有对应语音包。')
			os.system(path)

		# 打开文件夹
		elif ask == 'code':
			# smallize()
			os.system('start ' + r'C:\MySoftware\Notepad++/notepad++.exe D:\#My\GiData\Creation\Projects\Python\Gina\GiFun\GMain\gmain.py')
		elif ask == 'tools':
			# smallize()
			os.system('start ' + r'C:\MySoftware\Notepad++/notepad++.exe D:/#My/python_work/Gina/Tools.py')
		elif ask == 'tip':
			# smallize()
			os.system('start ' + r'C:\MySoftware\Notepad++/notepad++.exe D:/#My/python_work/Data_Technology/temptxt.py')

		elif ask == 'path':
			# smallize()
			os.startfile(r'..')
		elif ask == 'data':
			pan = 'D:\\#My\\GiData'
			speech.say('fddir',t='x')
			find_it = input('Find: ')
			find_dir(pan,find_it,showlen=3)
		elif ask == 'dataf':
			pan = 'D:\\#My\\GiData'
			find_it = input('Find: ')
			find_file(pan,find_it)
		elif ask == 'ddata':
			pan = 'D:\\'
			find_it = input('Find: ')
			find_dir(pan,find_it)


		elif ask == 'wp':  # wallpaper
			# smallize()
			os.startfile(r'C:/Users/111/Pictures/屏保')
		

		elif ask == 'test':
			# smallize()
			os.system('start ' + r'C:\MySoftware\Notepad++/notepad++.exe D:\#My\GiData\Creation\Projects\Python\Test\test.py')

		elif ask == 'qs':
			# smallize()
			os.startfile('C:\\quickstart')
			
		

		elif ask == 'py':
			# smallize()
			os.startfile('D:/#My/python_work')

		elif ask == 'my':
			# smallize()
			os.startfile('D:/#My')

		

		elif ask == 't0':
			# smallize()
			os.startfile('D:/#My/python_work/temp_0')

		elif ask == 't1':
			# smallize()
			os.startfile('D:/#My/python_work/temp_1')

		elif ask == 'cash':
			# smallize()
			os.startfile('D:/#My/python_work/Data_Technology/cash')

		elif ask == 'sth':
			dir = 'D:\\#My\\GiData\\Creation\\Illustrations\\sth\\'
			flist = os.listdir(dir)
			mode = input('Sth:')
			while mode != 'q':
				if mode == 'new':
					t = speech.timelog()
					tname = dir + t + '.txt'
					with open(tname, 'w') as f:
						thing = '##  ##\n@..@\n$\n'
						f.write(thing)
					os.system('start C:/quickstart/np.lnk ' + tname)
				elif mode == 'path':
					os.startfile(dir)
				elif mode == 'show':
					for f in flist:
						with open(dir + f, 'r', encoding='utf-8') as txt:
							stuff = txt.read()
						# print(stuff)
						get_title = re.search('##(.*)##', stuff)
						get_tag = re.search('@(.*)@', stuff)
						title = get_title.group()[2:-2].strip()
						tags = get_tag.group()[1:-1]
						tag = tags.split('.')
						text = stuff.split('$')[-1].strip()
						timet = f.split('.txt')[0]
						time = timet[:4] + '-' + timet[4:6] + '-' + timet[6:8] + ' ' + timet[8:10] + ':' + timet[10:12] + ':' + timet[12:]
						print('=' * 16 + str(flist.index(f)) + '=' * 16)
						print('Title: ' + title)
						print('Time: ' + time)
						print('Tags: ' + str(tag))
						print('Text: \n' + text)
						print('=' * 35)
						print('\n')
				elif 'op' in mode:
					try:
						open_i = int(mode[2:])
						os.system('start C:/quickstart/np.lnk ' + dir + flist[open_i])
					except:
						print('...')
				mode = input('\nSth:')


		# 打开网页
		elif ask == 'mp4':
			# 根据URL下载视频：支持逼站等
			url = input('URL: ')
			os.system('you-get -i ' + url)
			while url != 'q':
				url = input('>>>')
				os.system(url)
			os.startfile(os.getcwd())
		elif ask in webs:
			# smallize()
			os.system('start C:/quickstart/gg.lnk ' + web_dic[ask])


		elif ask[:3] == 'bd ':
			# smallize()
			say('baidu',t='x')
			bdurl = 'start C:/quickstart/gg.lnk https://www.baidu.com/s?wd=' + ask[3:]
			os.system(bdurl)

		elif ask == 'home':
			os.system('start C:/quickstart/gg.lnk ' + 'https://zacharychiu.github.io')
		
		elif ask == 'webs':
			os.system('start C:/quickstart/gg.lnk ' + 'https://zacharychiu.github.io/webs.html')

		elif ask == 'asd':
			# k.press_key(k.alt_l_key)
			# k.press_key(k.enter_key)
			# k.release_key(k.enter_key)
			# k.release_key(k.alt_l_key)
			speech.say('zhuangbility')
			os.system('color 02')
			nums = ''
			lines = 1000
			delay = 0.2
			print("Loading...")
			time.sleep(0.4)
			print('...')
			time.sleep(0.3)
			# say('check')

			for ts in range(lines):
				lenth = random.randint(10, 161)
				for i in range(lenth):
					it = random.randint(0, 1)
					nums += str(it)
				print(nums)
				if ts < 10:
					delay = delay * 0.97
				elif lines - ts < 8:
					delay += 0.05
				else:
					if delay > 0.01:
						delay = delay * 0.95
				time.sleep(delay)
				nums = ''

			time.sleep(0.4)
			for i in range(21):
				time.sleep(0.4)
				print('\r正在分析环境：{0}  {1}%'.format('▉' * i, (i * 5)), end='')
			print('\n')
			for i in range(21):
				time.sleep(0.3)
				print('\r正在计算塌陷方程：{0}  {1}%'.format('▉' * i, (i * 5)), end='')
			print('\n')
			for i in range(21):
				time.sleep(0.3)
				print('\r病毒程序写入中：{0}  {1}%'.format('▉' * i, (i * 5)), end='')
			time.sleep(0.5)
			print('\nSuccess...\n\n\n')
			time.sleep(1)
			os.system('color 04')
			f = open(r"C:\\Users\\111\\Documents\\桌面文件\\PIC.txt", 'r', encoding='utf-8')
			kulz = f.read()
			print(kulz)
			input('...')
			os.system('color 70')
		elif ask == 'off':
			confirm = input('你确定要我帮你关机吗？')
			if confirm == 'y':
				# smallize()
				os.system('start python D:/#My/python_work/pics/PygameGif.py')
				time.sleep(5)
				k.press_key(k.alt_l_key)
				k.press_key('c')
				k.release_key(k.alt_l_key)

				time.sleep(10)
				os.system('shutdown /s /t 10')

		elif ask == 'sleep':
			confirm = input('待会儿见咯~')
			os.system('rundll32 powrprof.dll,SetSuspendState')
		elif ask == 'web':
			os.system('start C:\\quickstart\\gg.lnk https://zacharychiu.github.io/')
		elif ask == 'cxk':
			rd = ''
			for i in range(12):
				n = random.randint(0, 9)
				rd += str(n)
			pyperclip.copy(rd + '@qq.com')
			print(rd)
			os.system('start C:\\quickstart\\gg.lnk https://cxkssr.xyz/auth/register')
		elif ask == 'cxkv':
			rd = ''
			for i in range(12):
				n = random.randint(0, 9)
				rd += str(n)
			pyperclip.copy(rd + '@qq.com')
			print(rd)
			os.system('start C:\\quickstart\\gg.lnk http://cxkv2.xyz/auth/register')
		elif ask == 'sound':
			# for i in range(50):
			#     os.system('color ' + str(i + 1))
			mu = os.listdir('D:\\#My\\GiData\\Creation\\Designs\\Audios')
			musics = []
			music_type = ['mp3','wmv']
			for m in mu:
				if m.split('.')[-1].lower() in music_type:
					musics.append(m)
			for i in range(len(musics)):
				print('%d【%s】' %(i,musics[i]))
			num = input('Index:')
			while num != 'q':
				if '.' not in num:
					if int(num):
						m_name = musics[int(num)]
						play_music('D:\\#My\\GiData\\Creation\\Designs\\Audios\\'+m_name)
				else:
					ns = num.split('.')
					for n in ns:
						if int(n):
							m_name = musics[int(n)]
							path = 'D:\\#My\\GiData\\Creation\\Designs\\Audios\\' + m_name
							play_music(path)
							audio = MP3(path)
							length = float(audio.info.length)
							time.sleep(length)
				num = input('Index:')

		elif ask not in order_collection:
			name = 'tts_logs\\'+str(speech.timelog()) + '.mp3'
			ans = chatme.chat(ask)
			
			
			# 检测音库是否已有
			with open('tts_logs\\log_dic.txt','r',encoding='utf-8') as f:
				log_list = f.readlines()
				logname = []
				logcontent = []
				for l in log_list:
					if l[0] != '#':
						aaa = l.split('\t')[0]
						bbb = '\t'.join(l.split('\t')[1:]).strip()
						if bbb not in logcontent:
							logcontent.append(bbb)
							logname.append(aaa)
			if ans in logcontent:
				speech.say('tts_logs\\'+logname[logcontent.index(ans)],dir='',t='x')
			else:
				log_name = speech.speak(ans,name='tts_logs\\[Chat]'+speech.timelog(),dir='',t='x').split('\\')[-1]
				with open('tts_logs\\log_dic.txt','a',encoding='utf-8') as f:
					f.write(log_name+'\t'+ans+'\n')
				print('-'*50)
			print('$ 姬娜:', ans, '\n')
	except Exception as e:
		print(e.args)
		print('...\n')


input()
