
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Zachary

'''
本程序通过文件名来识别标签，并将符合标签要求的文件以快捷方式的形式汇总到缓存文件夹。
目前的问题：
将符合筛选条件的图片的快捷方式集中放置到缓存文件夹，只能通过预览图查看所有项目，
使用图片浏览器（2345）查看后，点击“上一张图”或“下一张图”，仍然会显示源文件夹中的所有图片文件，不能实现只浏览缓存文件夹的图片。
【目前写了个基于pygame的瀑布流图片查看器以解决筛选图片连续查看问题。但是预览图画质不好】
>>> 使用快捷方式是基于程序运行速度的考虑。如果是直接把符合条件的文件完整复制到缓存文件夹，程序运行将会很慢（通常处理文件数上千）。
>>> 不过采用复制法就不存在上述问题。
'''
try:
	from shutil import copyfile
	import os
	import sys
	import pythoncom
	from win32com.shell import shell
	from win32com.shell import shellcon
	import win32com.client 
	from hashlib import md5
	from os.path import join, getsize
	import threading
	import random
	from PIL import Image
	import pyperclip
	from bs4 import BeautifulSoup
	from aip import AipFace
	import base64

	sys.setrecursionlimit(100000)

	def find_file(pan,filename):
		i = 0
		result = []
		for root, lists, files in os.walk(pan):
			for file in files:
				if filename == file:
					result = os.path.join(root, file)
		if result == []:
			print('not found!')
		else:
			return result

	## 读取配置文件 ##
	def a(tag):
		# 获取配置文件结构树（基于html标签系统）
		try:
			r = eval(tag.string.strip())
		except:
			r = tag.string.strip()
		return r


	with open(find_file('D:\\#My\\GiData\\Creation\\Projects\\Python\\Gina','config.ini'), encoding='utf-8') as f:
		text = f.read()
	ini = BeautifulSoup(text, 'html.parser')


	def _int(l):
		# 将列表所有元素转化为整型
		for i in range(len(l)):
			try:
				l[i] = int(l[i])
			except:
				l[i] = 0
		return l


	def ad_n(n, fn):
		tag_dic = ini.alltag.string.split('.')
		nl = fn.split('.')
		if nl[-2] not in tag_dic:
			# 不要误删标签
			nl[-2] = str(n)
		else:
			nl[-2] = nl[-2] + '.'+ str(n)
		r = '.'.join(nl)
		print(fn,'>>>',r)
		os.rename('..\\'+fn,'..\\'+r)
		return r

	def son_dir(father):
		i = 0
		result = []
		for root, lists, files in os.walk(father):
			for jia in lists:
				write = os.path.join(root, jia)
				result.append(write)
		return result
	

	def help():
		print('='*50)
		print(ini.help.string)
		print('='*50)


	def set_shortcut(filename,lnkname,iconname = ""):  # 如无需特别设置图标，则可去掉iconname参数
		try:
			# filename = r"D:\AppServ\timer\win_cron_zq\timer.exe"  # 要创建快捷方式的文件的完整路径
			# iconname = ""
			# lnkname = r"C:\Users\pc1\Desktop" + r"\timer.exe.lnk"  # 将要在此路径创建快捷方式

			shortcut = pythoncom.CoCreateInstance(
				shell.CLSID_ShellLink, None,
				pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
			shortcut.SetPath(filename)

			shortcut.SetWorkingDirectory(r"D:\AppServ\timer\win_cron_zq") # 设置快捷方式的起始位置, 不然会出现找不到辅助文件的情况
			shortcut.SetIconLocation(iconname, 0)  # 可有可无，没有就默认使用文件本身的图标
			if os.path.splitext(lnkname)[-1] != '.lnk':
				lnkname += ".lnk"
			shortcut.QueryInterface(pythoncom.IID_IPersistFile).Save(lnkname, 0)

			return True
		except Exception as e:
			print(e.args)
			return False

	'''清空文件夹函数'''
	def clear_cash(view_path):
		cash_name_list = os.listdir(view_path)
		for c in cash_name_list:
			cash_path = view_path+'/'+c
			os.remove(cash_path)

	def clean(l):
		img = ini.ft.string.split('.')
		new = []
		for i in l:
			if '.' in i:
				type = i.split('.')[-1]
			else:
				type = ''
			if type in img:
				new.append(i)
		return new

	def addtag(tags,v_path,do=True):
		Tags = tags.split('.')
		f_list = clean(os.listdir(o_path)) #获取文件夹内所有文件名
		c_list = []
		for tag in Tags:	#一个一个目标标签来
			for file_name in f_list:
				file_tag = file_name.split('.')
				if tag in file_tag:
					c_list.append(file_name)
			f_list = c_list[:]
			c_list = []
		# for i in f_list:
			# print(i)
		# print('*'*50)
		print('\n')
		if do == True:
			if f_list:
				#搬运
				for t in range(len(f_list)):	
					old_file_name = o_path + '\\' + f_list[t]
					percent = int(((t+1)/len(f_list)*100)/5)
					perc = '★'*percent+'☆'*(20-percent)
					
					# print('\r进度【'+str(percent)+'】','| 提取：',old_file_name[41:])
					print('\r进度【'+perc+'】',end='')
					new_file_name = os.getcwd() + '\\' + v_path+'\\'+f_list[t]		#创建快捷方式必须使用绝对路径！！！！！！！！！
					# print('source:',old_file_name)
					# print('goal:',new_file_name)
					set_shortcut(old_file_name,new_file_name)#创建快捷方式
					# copyfile(old_file_name,new_file_name)
			print('\n')
		return f_list

	def ortag(tags,v_path,do=True):
		Tags = tags.split('.')
		f_list = clean(os.listdir(o_path))#获取源文件夹内所有文件名
		c_list = []
		for tag in Tags:	#一个一个目标标签来
			for file_name in f_list:
				file_tag = file_name.split('.')
				if tag in file_tag:
					c_list.append(file_name)
		f_list = c_list[:]
		
		print('\n')
		if do == True:
			if f_list:
				#搬运
				for t in range(len(f_list)):	
					old_file_name = o_path + '\\' + f_list[t]
					# print('进度【'+str(t+1)+'/'+str(len(f_list))+'】','| 提取：',old_file_name[41:])
					percent = int(((t+1)/len(f_list)*100)/5)
					perc = '★'*percent+'☆'*(20-percent)
					
					print('\r进度【'+perc+'】',end='')
					new_file_name = os.getcwd() + '\\' + v_path+'\\'+f_list[t]
					set_shortcut(old_file_name,new_file_name+'.lnk')#创建快捷方式
					# copyfile(old_file_name,new_file_name)
			print('\n')
		return f_list


	def round(tag,f_list):
		for file_name in f_list:
			file_tag = file_name.split('.')
			if tag in file_tag:
				f_list.remove(file_name)
				round(tag,f_list)
				
	def minustag(tags,v_path,do=True):
		Tags = tags.split('.')
		f_list = clean(os.listdir(o_path))#获取源文件夹内所有文件名
		c_list = f_list[:]
		for tag in Tags:	#一个一个目标标签来
			round(tag,f_list)
		print('\n')
		if do == True:
			if f_list:
				#搬运
				for t in range(len(f_list)):	
					old_file_name = o_path + '\\' + f_list[t]
					# print('进度【'+str(t+1)+'/'+str(len(f_list))+'】','| 提取：',old_file_name[41:])
					percent = int(((t+1)/len(f_list)*100)/5)
					perc = '★'*percent+'☆'*(20-percent)
					
					print('\r进度【'+perc+'】',end='')
					new_file_name = os.getcwd() + '\\' + v_path+'\\'+f_list[t]
					set_shortcut(old_file_name,new_file_name+'.lnk')#创建快捷方式
			print('\n')
		return f_list

	def new(l_path,new_tag):
		
		lost_name_list = os.listdir(l_path)
		for lose in lost_name_list:	#lose中包含有.lnk
			pre = ''
			shell = win32com.client.Dispatch("WScript.Shell")
			path = l_path+'/'+lose
			shortcut = shell.CreateShortCut(path)
			target = shortcut.Targetpath
			# print(target)
			path_name = target.split('\\')
			heads = path_name[:-1]
			for head in heads:
				pre = pre+head+'/'
			botton = path_name[-1]
			new_name = pre+new_tag+'.'+botton
			# print('进度【',lost_name_list.index(lose)+1,'/',len(lost_name_list),'】 | ','重命名：',target)
			percent = int(((lost_name_list.index(lose)+1)/len(lost_name_list)*100)/5)
			perc = '★'*percent+'☆'*(20-percent)
			
			print('\r进度【'+perc+'】',end='')
			print('\n>>>：',new_name,'\n')
			os.rename(target,new_name)

	def get(get_path,for_path):
		lost_name_list = os.listdir(get_path)
		for lose in lost_name_list:	#lose中包含有.lnk
			pre = ''
			shell = win32com.client.Dispatch("WScript.Shell")
			path = get_path+'\\'+lose
			shortcut = shell.CreateShortCut(path)
			target = shortcut.Targetpath
			print(target)
			path_name = target.split('\\')
			file = path_name[-1]
			new_path = for_path+'\\'+file
			
			percent = int(((lost_name_list.index(lose)+1)/len(lost_name_list)*100)/5)
			perc = '★'*percent+'☆'*(20-percent)
			
			print('\r进度【'+perc+'】',end='')
			
			copyfile(target,new_path)
			# os.rename(target,new_name)


	def cutname(c_path,cut_tag):
		
		cut_name_list = os.listdir(c_path)
		for cut_name in cut_name_list:	#包含有.lnk
			pre = ''
			build = ''
			goal = ''
			shell = win32com.client.Dispatch("WScript.Shell")
			path = c_path+'/'+cut_name
			shortcut = shell.CreateShortCut(path)
			target = shortcut.Targetpath
			# print(target)
			path_name = target.split('\\')
			heads = path_name[:-1]
			for head in heads:
				pre = pre+head+'/'
			botton = path_name[-1]
			parts = botton.split('.')
			if cut_tag in parts:
				parts.remove(cut_tag)
				build = parts[0]
				for part in parts[1:]:
					build = build+'.'+part
			else:
				print('提示：输入的标签不存在于文件名中')
			new_name = pre+build
			print('重命名：',target)
			print('>>>',new_name,'\n')
			os.rename(target,new_name)



	def getdirsize(dir):
		size = 0
		for root, dirs, files in os.walk(dir):
			size += sum([getsize(join(root, name)) for name in files])
		return size


	def size(filelist,s,m='=',do=0):
		result = []
		if s[-1] == 'k':
			ss = int(s[:-1]) * 1024
		elif s[-1] == 'm':
			ss = int(s[:-1]) * 1024 * 1024
		for i in range(len(filelist)):
			size = os.path.getsize(os.path.join(o_path,filelist[i]))
			if m == '=':
				if size == ss:
					result.append(filelist[i])
			elif m == '>':
				if size >= ss:
					result.append(filelist[i])
			elif m == '<':
				if size <= ss:
					result.append(filelist[i])
		print('\n')
		if do == True:
			if result:
				#搬运
				for t in range(len(result)):	
					old_file_name = o_path + '\\' + result[t]
					percent = int(((t+1)/len(result)*100)/5)
					perc = '★'*percent+'☆'*(20-percent)
					
					print('\r进度【'+perc+'】',end='')
					new_file_name = os.getcwd() + '\\' + view_path+'\\'+result[t]
					set_shortcut(old_file_name,new_file_name+'.lnk')#创建快捷方式
			print('\n')
		return result
			

	def same(path1):
		'''================================'''
		ddd = int(input('查重模式（1为校对模式，0为删除模式）：'))
		'''================================'''
		list = []
		list1 = []

		# 得到所有图片的路径，加到列表list1中
		files = clean(os.listdir(o_path))
		for file in files:
			list1.append(file)

		# 计算每张图片的md5值，并将图片路径与其md5值整合到列表list中
		for n in range(len(list1)):
			hash = md5()
			img = open(o_path+'\\'+list1[n], 'rb')
			hash.update(img.read())
			img.close()
			list2 = [list1[n], hash.hexdigest()]
			# f.write(str(list2)+'\n')
			list.append(list2)
		print('\n=======================\n')
		for i in list:
			print(i)
		# 两两比较md5值，若相同，则删去一张图片
		m = 0
		while m < len(list):
			t = m + 1
			while t < len(list):
				if list[m][1] == list[t][1]:
					if ddd == 0:
						os.remove(o_path + '\\' + list[t][0])
					elif ddd == 1:
						o_path1 = o_path + '\\' + list[m][0]
						n_path1 = os.getcwd() + '\\' + path1+'\\'+list[m][0]
						o_path2 = o_path + '\\' + list[t][0]
						n_path2 = os.getcwd() + '\\' + path1+'\\'+list[t][0]+'【R】'
						set_shortcut(o_path1,n_path1+'.lnk')#创建快捷方式
						set_shortcut(o_path2,n_path2+'.lnk')
					
					print('检测出【',list[m][0],'】与【',list[t][0],'】重复')
					del list[t]
				else:
					t += 1
			m += 1
		if ddd == 1:
			os.startfile(view_path)
		elif ddd == 0:
			clear_cash(view_path)
			print('已删除重复文件，并清理缓存文件夹。')
			
	def get_drawed(fn):
		main_pos = 0
		ids0 = []
		ids = []
		with open(fn,'r',encoding='utf-8') as ini:
			line_list = ini.readlines()
			# print('读行：',line_list)
			for line in line_list:
				if line == '<main>\n':
					main_pos = line_list.index(line)+1
					# print('定位：',main_pos,'行')
			if main_pos != 0:
				for drawed in line_list[main_pos:]:
					if drawed != '\n':
						if '\n' in drawed: 
							drawed = drawed.replace('\n','')
						ids0.append(drawed)
						
						
		
		for i in ids0:
			i_list = i.split('  ')
			for j in i_list:
				j = j.replace(' ','')
				if j != '':
					ids.append(j)
		return ids
		
	def get_md5(file):
		hash = md5()
		f = open(file, 'rb')
		hash.update(f.read())
		f.close()
		HSkey = hash.hexdigest()
		return HSkey

	def scan_all(flist,svPath='HSkeyLibrary.csv'):
		csv_main_list = []
		
		for f in flist:
			index = f.split('.')[-2]
			key = get_md5(o_path + '\\' + f)
			csv_main_list.append(index+','+key)
		csv_main = '\n'.join(csv_main_list)
		csv = 'Index,HSkey\n' + csv_main
		print(csv)
		with open('HSkeyLibrary.csv','w') as HS:
			HS.write(csv)

	def find_id(HS,flist):
		i = ''
		for f in flist:
			fullpath = o_path + '\\' + f
			its_HS = get_md5(fullpath)
			if its_HS == HS:
				i = f.split('.')[-2]
		if i == '':
			print('人……人家没有找到……')
		print("序号是",i)
				
	def face(picpath):
		APP_ID = '15897329'
		API_KEY = 'xtNaN8HBQ7rSr9L0R4R8OmVj'
		SECRET_KEY = 'qtk2DUfSFPGFbqw007mSuLdgEMECtQOn'
		client = AipFace(APP_ID, API_KEY, SECRET_KEY)
		with open(picpath,"rb") as f:
			base64_data = base64.b64encode(f.read())
		image = str(base64_data,'utf-8')
		imageType = "BASE64"
		client.detect(image, imageType)
		options = {}
		options["face_field"] = "age,beauty,gender,race,quality,facetype"
		options["max_face_num"] = 1
		options["face_type"] = "LIVE"
		result = client.detect(image, imageType, options)
		try:
			gender = result['result']['face_list'][0]['gender']['type']
			age = result['result']['face_list'][0]['age']
			beauty = result['result']['face_list'][0]['beauty']
		except:
			gender = '未识别到人脸'
			age = '未识别到人脸'
			beauty = '未识别到人脸'
		return [gender,age,beauty]
		
	'''正文'''
	'''============================================'''
	#注：以下两个路径精确到文件夹，且不要以‘/’结尾

	view_path = 'cash\\cash0' 				#最终的浏览文件夹


	o_path = '\\'.join(os.getcwd().split('\\')[:-1])

	special = ['d-','y-','s-','n-','f-','w-','edt-']

	# drawed = get_drawed('random_drawing.ini')	# 根据ini文件获取已经画过的随机抽画图片的序号，用以防止随机抽取抽到已经画过的图
	'''============================================'''
	print('当前位置：'+o_path)
	print('缓存目录：',view_path)

	tag_txt = input('请输入标签↓\n>>>').strip().lower()
	mode = input('模式：')
	# print('#'+mode+'#')
	########
	# mode = 'test'
	while mode != 'q':
		md = mode.split(' ')
		try:
			if mode == 'test':
				s = tag_txt
				p = o_path
				flist = clean(os.listdir(p))
				for f in flist:
					type = f.split('.')[-1]
					if type.lower() != type:
						print('>>>'+f)
						# os.rename(p+'\\'+f,p+'\\'+f.lower())
				# print(flist)
			elif mode == 'cg':
				print('请选择缓存目录：')
				choice = son_dir('cash')
				for i in range(len(choice)):
					print('%d\t%s'%(i,choice[i]))
				c = input('缓存目录改为：')
				try:
					re = int(c)
					if re in range(len(choice)):
						view_path = choice[re]
				except:
					pass
			elif mode == 'cgo':
				print('请选择源目录：')
				choice = son_dir('D:\\#My\\GiData\\Source\\Arts\\Images')
				for i in range(len(choice)):
					if choice[i].split('\\')[-2] == 'Images':
						print('%d\t%s'%(i,choice[i]))
				c = input('源目录改为：')
				try:
					re = int(c)
					if re in range(len(choice)):
						o_path = choice[re]
					else:
						o_path = '\\'.join(os.getcwd().split('\\')[:-1])
				except:
					for i in range(len(choice)):
						if choice[i].split('\\')[-2] == 'Images':
							if choice[i].split('\\')[-1] == 'Pics':
								o_path = choice[i]
				
				

			elif mode == 'help':
				help()
			elif mode == 's':
				os.system('start PicFlow.py')
			elif md[0] == 'size':
				filelist = clean(os.listdir(o_path))
				if len(md) == 1:
					s = tag_txt
					r = size(filelist,s,m='>')
					print(len(r))
				elif len(md) > 2:
					# 'size + >'
					s = tag_txt.split(' ')[0]
					try:
						t = tag_txt.split(' ')[1]
						if md[1] == '+':
							filelist = addtag(t,view_path,do=0)
						elif md[1] == '-':
							filelist = minustag(t,view_path,do=0)
						elif md[1] == '/':
							filelist = ortag(t,view_path,do=0)
					except:
						# 没有指定标签要求
						pass
					
					if md[-1] == 'do':
						r = size(filelist,s,m=md[2],do=True)
						os.startfile(view_path)
					else:
						r = size(filelist,s,m=md[2])
					print(len(r))
			elif md[0] == '-':
				if len(md) == 1:
					clear_cash(view_path)
					minustag(tag_txt,view_path)
					os.startfile(view_path)
				else:
					if md[1] == 'c':
						result = minustag(tag_txt,view_path,do=0)
						print('符合条件的结果数：%d'%len(result))
					elif md[1] == 'face':
						p = o_path
						result = minustag(tag_txt,view_path,do=0)
						for f in result:
							yan = face(p+'\\'+f)
							print(f.split('.')[-2],'>>>',yan[-1])
			elif md[0] == '+':
				if len(md) == 1:
					clear_cash(view_path)
					addtag(tag_txt,view_path)
					os.startfile(view_path)
				else:
					if md[1] == 'c':
						result = addtag(tag_txt,view_path,do=0)
						print('符合条件的结果数：%d'%len(result))
					elif md[1] == 'face':
						p = o_path
						result = addtag(tag_txt,view_path,do=0)
						for f in result:
							yan = face(p+'\\'+f)
							print(f.split('.')[-2],'>>>',yan[-1])
			elif md[0] == '/':
				if len(md) == 1:
					clear_cash(view_path)
					ortag(tag_txt,view_path)
					os.startfile(view_path)
				else:
					if md[1] == 'c':
						result = ortag(tag_txt,view_path,do=0)
						print('符合条件的结果数：%d'%len(result))
						p = o_path
						result = ortag(tag_txt,view_path,do=0)
						for f in result:
							yan = face(p+'\\'+f)
							print(f.split('.')[-2],'>>>',yan[-1])
			elif mode == 'new':
				new(view_path,tag_txt)
				clear_cash(view_path)
				os.startfile(o_path)
			elif mode == 'get':
				clear_cash('cash\\get')
				get(view_path,'cash\\get')
				os.startfile('cash\\get')
			elif mode == 'num':
				# 根据序号集提取文件
				print('')
				clear_cash(view_path)
				num_list = tag_txt.split('.')
				for n in num_list:
					addtag(n,view_path)
				clear_cash('cash\\get')
				get(view_path,'cash\\get')
				os.startfile('cash\\get')
			elif mode == 'c':
				clear_cash(view_path)
				print('已清空缓存文件夹')
			elif mode == 'call':
				clear_cash('cash\\cash0')
				clear_cash('cash\\cash1')
				clear_cash('cash\\cash2')
				clear_cash('cash\\get')
				print('已清空缓存文件夹')
			elif mode == 'op':
				os.startfile(o_path)
			elif mode == 'opc':
				os.startfile(view_path)
			elif mode == 'tag':
				# os.system('start Tags.ini')
				tag_trans = { 'VhiTvm':'张腿','anqr':'安全','babi':'扒屄','bii':'屄','buru':'哺乳',
					'ccbi':'肏屄','ceu':'侧','dautvm':'大腿','dyi':'蹲','f-80':'端正',
					'f-85':'不错','f-90':'漂亮','f-95':'超美','fum':'俯','fur':'伏',
					'gsvs':'公众','gvu':'跪','h-sjfa':'发型-散发','hjrffi':'韩风',
					'hvjp':'灰阶','hztu':'厚涂','i':'单女','i_o':'1.0身','i_s':'1.5身',
					'iahx':'插画','ie':'18X','ifitzr':'撑头','is':'15度脸','iyr':'纯女性',
					'jind':'挤奶','jo ':'正侧脸','juuzM':'举手','kzbi':'抠屄','kzmjni':'口交',
					'liu':'立','lnifau':'撩发','m_d':'3D','mix':'男女混合','mwmuiu':'美式',
					'mwtiM':'美体','n-2b':'人物-2b','n-darjim':'人物-妲己','n-sabar':'人物-Sabar',
					"n-x'izmnvm":'人物-小丑女','ndmz':'奶子','ndxb':'奶心','o':'零件',
					'o_i':'头像','o_s':'0.5身','pigu':'屁股','pni':'飘','qs':'75度脸',
					'quu':'有趣','r':'多女','r_o':'全身像','riuiU':'日式','s-bbxtqiyr':'冰雪奇缘',
					's-disini':'迪斯尼','s-gvmdci':'鬼刀','s-gvmpvirf ':'鬼灭之刃',
					's-halibote ':'哈利波特','s-lol ':'英雄联盟','s-lsrvui':'龙珠',
					's-maliao':'马里奥','s-marvel':'漫威','s-mouzuijp':'魔兽世界',
					's-naruto':'火影忍者','s-onepunch':'一拳超人','s-overwatch':'守望先锋',
					's-ufqibcbw':'神奇宝贝','s-ybxsxtyr':'','sdlu':'赛璐璐','suti':'素体',
					'thm':'躺','tmmbii':'舔屄','show':'展示','tzis':'15度脸','tzo':'正脸',
					'uiti':'实体','us':'45度脸','w-bdr':'袜子-白色','w-buuwau':'袜子-布袜',
					'w-cdm':'袜子-彩色','w-dnuddu':'袜子-吊带','w-hwi':'袜子-黑色',
					'w-hxiwfr':'袜子-花纹','w-lwrsii':'袜子-蕾丝','w-mmrwau':'袜子-棉袜',
					'w-pirger':'袜子-皮革','w-rsrwau':'袜子-绒袜','w-rzu':'袜子-肉色',
					'w-siwa':'袜子-丝袜','w-tnrwfr':'袜子-条纹','w-ujiger':'袜子-栅格',
					'w-whmger':'袜子-网格','wditzr':'歪头','wfuf':'纹身','xsibuu':'胸部',
					'xxx':'临时标记用','y-drmqyr':'服-短裙','y-icdrku':'服-超短裤',
					'y-icdrqy':'服-超短裙','y-nqzdku':'服-牛仔裤','y-nwku':'服-内裤',
					'y-qmrkdiqyr':'服-前开裙'
						}
				print(tag_trans)
			elif mode == 'tree':
				os.system('start Tags.emmx')
			elif mode == 'webp':
				Tags = tag_txt.split('.')
				f_list = clean(os.listdir(o_path)) #获取文件夹内所有文件名
				webp_list = []
				gif_list = []
				clean_list = []
				# 抽取图片
				for file_name in f_list:
					file_tag = file_name.split('.')
					if 'webp' in file_tag:
						webp_list.append(file_name)
				for w in webp_list:
					if '[gif]' in w:
						gif_list.append(w)
					else:
						clean_list.append(w)
				full_path = o_path
				m = input('1: 抽取webp静态图\n2: 抽取webp动态图\n选择：')
				
				
				# 提取图片
				if webp_list:
					if m == '1':
						print('='*30)
						for i in clean_list:
							print(i)
						print('='*30)
						yes = input('即将抽取以上文件，get文件夹将被清空，是否继续？[y/any]')
						
						if yes == 'y':
							clear_cash('cash\\get')
							for c in clean_list:
								copyfile(full_path+'\\'+c,os.getcwd()+'\\cash\\get\\'+c)
								os.remove(full_path+'\\'+c)
							os.startfile('cash\\get')
					elif m == '2':
						print('='*30)
						for i in gif_list:
							print(i)
						print('='*30)
						yes = input('即将抽取以上文件，get文件夹将被清空，是否继续？[y/any]')
						if yes == 'y':
							clear_cash('cash\\get')
							for c in gif_list:
								copyfile(full_path+'\\'+c,os.getcwd()+'\\cash\\get\\'+c)
								os.remove(full_path+'\\'+c)
							os.startfile('cash\\get')
				
			elif mode == 'cut':
				cutname(view_path,tag_txt)
				clear_cash(view_path)
				os.startfile(o_path)

			
			elif mode == 'all':
				clear_cash(view_path)
				file_name_list = clean(os.listdir(o_path))#获取a文件夹内所有文件名
				for name in file_name_list:	
					if '.' in name:
						old_file_name = o_path + '\\' + name
						new_file_name = os.getcwd() + '\\' + view_path+'\\'+name
						percent = int(((file_name_list.index(name)+1)/len(file_name_list)*100)/5)
						perc = '★'*percent+'☆'*(20-percent)
						
						print('\r进度【'+perc+'】',end='')
						set_shortcut(old_file_name,new_file_name+'.lnk')#创建快捷方式
				os.startfile(view_path)
			elif mode == 'same':
				clear_cash(view_path)
				same(view_path)
			elif mode == 'info':
				# 计算
				f_list = clean(os.listdir(o_path))
				size = getdirsize(o_path)
				
				def atag(tag):
					Tags = tag.split('.')
					f_list = clean(os.listdir(o_path)) #获取文件夹内所有文件名
					c_list = []
					for tag in Tags:	#一个一个目标标签来
						for file_name in f_list:
							file_tag = file_name.split('.')
							if tag in file_tag:
								c_list.append(file_name)
						f_list = c_list[:]
						c_list = []
					return len(f_list)
				
				def io_star(tag_list,all,theone):
					anqr = all - theone
					penc_theone = int(theone/all*100)
					star_theone = int(theone/all*10)
					bar = '★'*star_theone + '☆'*(10-star_theone)
					print('['+tag_list[0]+']-'+str(penc_theone)+'%|'+bar+'|'+str(100-penc_theone)+'%-['+tag_list[1]+']')

				def show_star(tag_list,bd_list):
					len_bd = 0
					tag_width = 0
					for i in tag_list:
						tag_w = len(i)
						if tag_w > tag_width:
							tag_width = tag_w
						
					for l in bd_list:
						len_bd += l
					bd_bar = []
					for i in range(len(bd_list)):
						penc = int(bd_list[i]/len_bd*100)
						star = int(bd_list[i]/len_bd*20)
						bar = '★'*star + '☆'*(20-star)
						if tag_width>len(tag_list[i]):
							blank0 = ' '*(tag_width-len(tag_list[i]))
						else:
							blank0 = ''
						if len(str(penc))<2:
							blank1 = ' '*(2-len(str(penc)))
						else:
							blank1 = ''
						bd_bar.append('['+tag_list[i]+blank0+']'+'-'+blank1+str(penc)+'%|'+bar)

					# print('tag宽度',tag_width)
					print('-'*(tag_width+47)) # 45=中括号两位加20个占两位的星星加上百分比占的五位
					for i in bd_bar:
						print(i)
					print('-'*(tag_width+47))

				# 显示
				print('\n路　　　径:',o_path)
				print('文件　数量:',len(f_list))
				print('文件夹大小：%.3f' % (size/1024/1024/1024),'G')
				io_star(['ie','anqr'],len(f_list),atag('ie'))
				io_star(['iyr','mix'],len(f_list),atag('iyr'))
				bd_l = ['r_o', 'i_s', 'i_o', 'o_s', 'o_i', 'o']
				bd_n = []
				for l in bd_l:
					bd_n.append(atag(l))
				show_star(bd_l,bd_n)
				art_l = ['iahx', 'uiti', 'm_d']
				art_n = []
				for l in art_l:
					art_n.append(atag(l))
				show_star(art_l,art_n)
				face_l = ['f-95','f-90','f-85','f-80']
				face_n = []
				for l in face_l:
					face_n.append(atag(l))
				show_star(face_l,face_n)
				p_l = ['i','r','mix']
				p_n = []
				for l in p_l:
					p_n.append(atag(l))
				show_star(p_l,p_n)
				
			elif mode in special:
				
				draw_name = []
				clear_cash(view_path)
				f_list = os.listdir(o_path)
				for f in f_list:
					if mode in f:
						draw_name.append(f)
						o_path = o_path+'/'+f
						n_path = view_path+'/'+f
						set_shortcut(o_path,n_path+'.lnk')#创建快捷方式
						print('提取:',f)
				os.startfile(view_path)
			
			
			elif mode == 'd':
				tag_txt = 'suutim.r_o.liu'
				clear_cash(view_path)
				addtag(tag_txt,view_path)
				os.startfile(view_path)
			elif mode == 'code':
				os.system(r'start C:\MySoftware\Notepad++/notepad++.exe '+find_file(o_path,'Tags_win.py'))
			elif mode == 'path':
				os.startfile('')
			elif mode == 'pi':
				import matplotlib as mpl
				import matplotlib.pyplot as plt
				import numpy as np
				plt.ion()	#这行代码使得不关闭图标窗口，主程序也会继续执行下去
				
				file_name_list = clean(os.listdir(o_path))#获取a文件夹内所有文件名
				flen = len(file_name_list)
				
				def rand_color(n=1):
					colors = []
					for i in range(n):
						colors.append((random.random(),random.random(),random.random()))
					return colors
							
				
				def contag(tagname):
					result = []
					for i in file_name_list:
						file_tags = i.split('.')
						if tagname in file_tags:
							result.append(i)
					return len(result)
				
				
				tag_groups = eval(ini.tag_group.string)  #标签分组信息（列表）
				ct_dic = {}  # 标签所含文件数量（字典）
				for tg in tag_groups:
					for t in tg:
						ct_dic[t] = contag(t)  #计数

				mpl.rcParams["font.sans-serif"] = ["SimHei"]
				mpl.rcParams["axes.unicode_minus"] = False
				
				#TEST
				for tg in tag_groups:
					parts = []
					partionnums = []
					for t in tg:
						parts.append(t+'\n('+str(ct_dic[t])+')')
						partionnums.append(ct_dic[t])
					colors = rand_color(len(tg))
					
					# 排列图表
					whole = len(tag_groups)
					h = int(whole**0.5)
					w = int(whole/h)+1
					# print('总共有%d个图表'%whole)
					# print('方阵高度设置为%d'%h)
					# print('方阵宽度设置为%d'%w)
					# 表示 绘制图像1行2列第1个
					pos = int(str(h) + str(w) + str(tag_groups.index(tg)+1))
					# print(pos)
					fig1 = plt.subplot(pos)
					plt.pie(partionnums,autopct="%3.1f%%",labels=parts,startangle=45,shadow=False,colors=colors,wedgeprops=dict(width=0.6,edgecolor='w'))
					plt.title(eval(ini.group_name.string)[tag_groups.index(tg)])
					plt.show()
				

			elif mode == 'set':
				# ppp = 'D:\\111\\Cash\\Temporary\\Background\\HlTuR\\aa'
				file_name_list = clean(os.listdir(o_path))#获取a文件夹内所有文件名
				flen = len(file_name_list)
				for fn in file_name_list:
					ftlist = fn.split('.')
					ftaglist = list(set(ftlist[:-2])) # 文件名标签去重
					ftaglist.sort()
					num = file_name_list.index(fn)
					newname = o_path+'\\'+'.'.join(ftaglist)+'.'+'.'.join(ftlist[-2:])
					
					## Test ##
					# print('newname: #'+newname+'#')
					if newname != fn:
						os.rename(o_path+"\\"+fn,newname)
					percent = int(((num+1)/len(file_name_list)*100)/5)
					perc = '★'*percent+'☆'*(20-percent)
					print('\r标签修剪中【'+perc+'】',end='')
					
		
				
			elif mode == 'fcut':
				# ppp = 'D:\\111\\Cash\\Temporary\\Background\\HlTuR\\aa'
				file_name_list = clean(os.listdir(o_path))#获取a文件夹内所有文件名
				flen = len(file_name_list)
				ftype = ['jpg','jpeg','png','gif','webp','jfif']
				fwrong = []
				
				def transnum(n):
					ftemps = {'0':'o','1':'i','2':'r','3':'m','4':'u','5':'s','6':'b','7':'q','8':'e','9':'j'}
					numstr = str(n)
					zacnumlist = []
					for i in numstr:
						zacnumlist.append(ftemps[i])
					zacnum = ''.join(zacnumlist)
					return zacnum
				for fn in file_name_list:
					ftaglist = fn.split('.')
					fend = ftaglist[-1]
					foname = ftaglist[-2]
					f3 = ftaglist[-3]
					num = file_name_list.index(fn)
					# print(transnum(num+1))
					newname = o_path+'\\'+'.'.join(ftaglist[:-2])+'.'+transnum(num+1)+'.'+ftaglist[-1]
					# print('newname:',newname)
					os.rename(o_path+"\\"+fn,newname)
					percent = int(((num+1)/len(file_name_list)*100)/5)
					perc = '★'*percent+'☆'*(20-percent)
					print('\r文件整理中【'+perc+'】',end='')
					
					
				file_name_list = clean(os.listdir(o_path))#获取a文件夹内所有文件名
				fwrong = []
				print('\n\n******************\n')
				for fn in file_name_list:
					ftaglist = fn.split('.')
					fend = ftaglist[-1]
					foname = ftaglist[-2]
					f3 = ftaglist[-3]
					num = file_name_list.index(fn)
					newname = o_path+'\\'+'.'.join(ftaglist[:-2])+'.'+str(num+1)+'.'+ftaglist[-1]
					# print('newname:',newname)
					os.rename(o_path+"\\"+fn,newname)
					percent = int(((num+1)/len(file_name_list)*100)/5)
					perc = '★'*percent+'☆'*(20-percent)
					print('\r修剪文件中【'+perc+'】',end='')
					
				# 更新Key列表
				print('\n更新Key列表中...\n')
				f_list = clean(os.listdir(o_path))
				scan_all(f_list,svPath=view_path)
				
				
			elif mode == 'sq':
				clear_cash(view_path)
				##筛选横向、竖向、方形图片
				target = []
				file_name_list = clean(os.listdir(o_path))#获取a文件夹内所有文件名
				for fn in file_name_list:
					try:
						img = Image.open(o_path+'\\'+fn)
						size = img.size
						if tag_txt == 'o':
							if 0.8 < size[0]/size[1] < 1.2:
								target.append(fn)
						if tag_txt == 'm':
							if size[0]/size[1] > 1.2:
								target.append(fn)
						if tag_txt == 'l':
							if size[0]/size[1] < 0.8:
								target.append(fn)
						percent = int(((file_name_list.index(fn)+1)/len(file_name_list)*100)/5)
						perc = '★'*percent+'☆'*(20-percent)
						print('\r计算中【'+perc+'】',end='')
					except:
						print('\nPass one image...\n')
				print('\n')
				print('*'*50)
				for tg in target:
					old_file_name = o_path + '\\' + tg
					percent = int(((target.index(tg)+1)/len(target)*100)/5)
					perc = '★'*percent+'☆'*(20-percent)
					print('\r提取中【'+perc+'】',end='')
					new_file_name = os.getcwd() + '\\' + view_path+'\\'+tg
					set_shortcut(old_file_name,new_file_name+'.lnk')#创建快捷方式
				os.startfile(view_path)
			
			elif mode == 're':
				print('\n\n')
				os.system('python '+find_file(o_path,'Tags_win.py'))
				
			
			elif mode == 'cs':
				if tag_txt == 'un':
					os.system('start python ..\\..\\unnamed\\TAGL\\Tags_Light.py')
				elif tag_txt == 'pic' or tag_txt == '':
					os.system('start python ..\\..\\Pics\\TAGL\\Tags_Light.py')
			elif mode == 'tem':
				clear_cash(view_path)
				file_name_list = clean(os.listdir(o_path))#获取a文件夹内所有文件名
				index = random.randint(0,len(file_name_list))
				addtag(str(index),view_path)
				# print(index)
				target = os.listdir(view_path)
				# print(target)
				os.system('start '+view_path+'\\'+target[0])
				
				
			elif mode == 'at':
				file_name_list = clean(os.listdir(o_path))#获取a文件夹内所有文件名
				tag_count = []
				for fn in file_name_list:
					fts = fn.split('.')[:-2]
					for t in fts:
						if t not in tag_count:
							tag_count.append(t)
					print('\r抽取：',file_name_list.index(fn)+1,'/',len(file_name_list),end='')
				tag_count.sort() # 按字母排序
				print('\n')
				for i in range(len(tag_count)-1):
					if i%5 != 0:
						print('\t| '+tag_count[i],end='')
					else:
						print('\t| '+tag_count[i])
			## 关联文件·专题 ##
			elif mode == 'scan':
				f_list = clean(os.listdir(o_path))
				scan_all(f_list,svPath=view_path)
				os.startfile(os.getcwd())
			
			elif mode == 'keys':
				os.system('HSkeyLibrary.csv')
			elif mode == 'HS':
				f_list = clean(os.listdir(o_path))
				for f in f_list:
					if f.split('.')[-2] == tag_txt:
						# print('Goal:'+f.split('.')[-2])
						key = get_md5(o_path + '\\' + f)
				pyperclip.copy(key)
				print(key)
				
			elif mode == 'fd':
				f_list = clean(os.listdir(o_path))
				lock = tag_txt
				for f in f_list:
					key = get_md5(o_path + '\\' + f)
					if key == lock:
						print('序号为：'+f.split('.')[-2])
			elif mode == 'tip':
				# 先根据序号找到文件名
				index = tag_txt.split('.')[0]
				try:
					op = tag_txt.split('.')[1]
				except:
					op = ''
				o_file = ''
				f_list = clean(os.listdir(o_path))
				for f in f_list:
					if f.split('.')[-2] == index:
						# print('Goal:'+f.split('.')[-2])
						o_file = f
				if o_file != '':
					key = get_md5(o_path + '\\' + o_file)
					# print('date\\tips\\'+key+'.txt')
					pyperclip.copy('<HS>'+key+'\n<main>\n')
					if op == 'o':
						# 此处使用notepad++打开文本，若无此文件，它自带新建功能，因此不用麻烦再写新建文件的代码了。
						os.system(r'start C:\MySoftware\Notepad++/notepad++.exe date\\tips\\'+key+'.ini')
						
					else:
						with open('date\\tips\\'+key+'.ini','r',encoding='utf-8') as t:
							text = t.read()
							tip = text.split('<main>')[-1]
						print('='*50)
						print(tip)
						print('='*50)
			
			
			elif mode == 'fff':
				rrrr = 0  # 是否有重复编号
				f_list = clean(os.listdir(o_path))
				indexs = []
				wro = []  # 
				for f in f_list:
					i = f.split('.')[-2]  # i是文件f的编号
					# print('获取到文件编号',i)
					try:
						i = int(i)
						if i <= len(f_list):
							# 防止把由数字（比如日期）组成的超级大数误认为编号
							indexs.append(i)
						else:
							indexs.append('X')
							wro.append(f_list.index(f))
					except:
						indexs.append('X')
						wro.append(f_list.index(f))
					
				if len(indexs) != len(list(set(indexs))):
					print('\n！！！悄悄地警告你一下：有重复编号。\n')
					rrrr = 1
				if rrrr:
					# 需要降重
					dict = {}  # 统计列表中所有元素出现次数，并存入字典
					to_change = {}
					for key in indexs:
						dict[key] = dict.get(key,0)+1
					for i in range(len(indexs)):
						if dict[indexs[i]] != 1:
							# print(indexs[i],'>>重复了%d次'%dict[indexs[i]])
							# print('她是%d号文件'%i)
							# print('她的芳名是：',f_list[i])
							# print('现在把她X掉。')
							#
							indexs[i] = 'X'
							wro.append(i)
				nums = list(set(_int(indexs[:])))
				# print(nums)
				if 0 in nums:
					nums.sort()
					nums.remove(0)
					# print('删除0...')
				# print('删除后的nums：',nums)
				print('！！！！！！开始重命名！！！！！')
				if not nums:
					# 所有文件都需要编号
					for j in range(len(wro)):
						ad_n(j+1,f_list[wro[j]])
				else:
					# 只有部分文件需要编号
					mid_n = []

					for i in range(nums[-1]):
						if i != 0:
							if i not in nums:
								mid_n.append(i)

					if len(wro) > len(mid_n):
						# 漏数不够用
						for i in range(len(mid_n)):
							# 把漏数用掉
							ad_n(mid_n[i],f_list[wro[i]])
						for j in range(len(wro)-len(mid_n)):
							# 给剩下的文件编号
							ad_n(nums[-1]+j+1,f_list[wro[len(mid_n)+j]])
					else:
						for i in range(len(wro)):
							ad_n(mid_n[i],f_list[wro[i]])


				# print('所有文件的序号：\n',indexs)
				# print('未使用的序号：\n',mid_n)
				# print('\n无序号的文件')
				# for w in wro:
					# print(f_list[w])
				print('#'*30)
				print('##########重命名完成！##########')
				print('#'*30)
			
			
			
			else:
				print('\n...\n\n')
			
		except Exception as e:
			print(e.args)
		print('\n'*2)
		print('#'*50)
		print('当前位置：'+o_path)
		print('缓存目录：',view_path)
		tag_txt = input('请输入标签↓\n>>>').strip().lower()
		mode = input('模式：')
except Exception as e:
	print(e)
	input()



	
