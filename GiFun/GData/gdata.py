#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Zachary

'''
本程序旨在管理我的数据库。
所有数据需汇聚到一个主文件夹‘DateBase’
'''
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
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup as bs
from hashlib import md5
from aip import AipFace
import base64
import cv2
import matplotlib.pyplot as plt  
import math
import pyperclip

APP_ID = '15897329'
API_KEY = 'xtNaN8HBQ7rSr9L0R4R8OmVj'
SECRET_KEY = 'qtk2DUfSFPGFbqw007mSuLdgEMECtQOn'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)
sys.setrecursionlimit(100000)

class Numbers():
	def __init__(self):
		pass
	def line(self,a,b):
		xa = range(a[0],b[0])
		ya = []
		for x in xa:
			y = (a[1]-b[1])*x/(a[0]-b[0])+(a[0]*b[1]-a[1]*b[0])/(a[0]-b[0])
			ya.append(y)
		return xa,ya

class Pic():
	def __init__(self,pic_path):
		self.path = pic_path
		self.name = os.path.split(self.path)[-1]
		self.loc = os.path.split(self.path)[:-1][0]
		self.it = self.read()
		self.size = self.it.size
		# print('!!!!!',self.loc)
	
	def cg(self,change):
		# 换图
		self.path = change
	
	def cgit(self,it):
		self.it = it
	
	def mk(self,w,h):
		# 创建空白图
		return Image.new(self.it.mode, (w, h))
	
	def read(self):
		# 加载图片
		img = Image.open(self.path)
		if img.mode == "P":
			img = img.convert('RGB')
		return img
	
	def cut(self,st,wh):
		# 剪裁
		# st:开始坐标；wh:宽高
		img = self.it.crop((st[0],st[1],st[0]+wh[0],st[1]+wh[1]))
		return img
	
	def resize(self,it=0,wh=(0,0),r=0,rw=0,rh=0):
		# 重定义大小
		
		if it == 0:
			it = self.it
		if r != 0:
			w,h = it.size
			return it.resize((int(w*r), int(h*r)), Image.BILINEAR)
		elif wh != (0,0):
			return it.resize((wh[0], wh[1]), Image.BILINEAR)
		elif rw != 0:
			w,h = it.size
			ratio = h / w
			new_h = int(rw * ratio)
			return it.resize((rw, new_h), Image.BILINEAR)
		elif rh != 0:
			w,h = it.size
			ratio = w / h
			new_w = int(rh * ratio)
			return it.resize((new_w, rh), Image.BILINEAR)
		else:
			return it
	
	def preview(self,aaa,ss=100):
		# 给定图片集，将她们拼接为一张图（附文件名）以供预览
		font_h = 25  #字体高度
		font_path = ImageFont.truetype("C:\\Windows\\Fonts\\msyh.ttc", 20)
		piclist = []
		ad = 0
		names = {}
		for i in aaa:
			try:
				im0 = self.mk(ss,ss + font_h)
				img = Pic(os.path.join(self.loc,i))
				if img.size[0] > img.size[1]:
					im1 = img.resize(rh=ss)
				else:
					im1 = img.resize(rw=ss)
				img.cgit(im1)
				im = img.cut((0,0),(ss,ss))
				im0.paste(im, box=(0, 0))
				draw = ImageDraw.Draw(im0)
				draw.text((0,ss), i.split('.')[-2], fill="#ffffff", font=font_path)
				piclist.append(im0)
				ad += 1
			except Exception as e:
				print(e)
				pass
		
		whole = len(piclist)  # 总量
		h = int(whole**0.5)		# 方阵边长
		w = int(whole/h)+1
		print('总共有%d个图'%whole)
		print('方阵有%d行%d列'%(h,w))
		blank = self.mk(ss*(w),(ss + font_h)*h)
		for i in range(len(piclist)):
			x = i % w
			y = i // w
			a = x * ss
			b = y * (ss+font_h)
			p = piclist[i]
			blank.paste(p, box=(a, b))
			print('序号【%d】放置位号(%d,%d)；放置坐标(%d,%d)'%(i,x,y,a,b))
		
		
		blank.save('test.jpg')
		return os.path.join(os.getcwd(),'test.jpg')
	
	def face_rect(self):
		nums = Numbers()
		imageType = "BASE64"
		with open(self.path,"rb") as f:
			base64_data = base64.b64encode(f.read())
			base = str(base64_data,'utf-8')
		options = {}
		options["face_field"] = "age,beauty,expression,face_shape,gender,glasses,landmark,landmark150,quality,eye_status,emotion,face_type,mask,spoofing"
		options["max_face_num"] = 1
		options["face_type"] = "LIVE"
		result = client.detect(base, imageType,options)['result']['face_list'][0]
		# print(result)
		location = result['landmark72']
		beauty = result['beauty']
		gender = result['gender']['type']
		age = result['age']
		
		mark_x,mark_y = [],[]
		for xy in location:
			mark_x.append(xy['x'])
			mark_y.append(xy['y'])
			
		top = min(mark_y)
		bottom = max(mark_y)
		left = min(mark_x)
		right = max(mark_x)
		w0 = right-left
		h0 = bottom-top
		
		# (x,y,w,h) = (x0,y0,w0*math.cos(angle*math.pi/180)+h0*math.sin(angle*math.pi/180),h0*math.cos(angle*math.pi/180)+w0*math.sin(angle*math.pi/180))
		(x,y,w,h) = (left,top,w0,h0)
		# self.paint_rect(x,y,w,h)
		# 将图片显示在matplotlib中，并画上标记
		img=cv2.imread(self.path)
		(r,g,b)=cv2.split(img)
		img=cv2.merge([b,g,r])
		plt.axis('off')  # 关闭坐标轴
		plt.title('Pic') 
		plt.imshow(img)
		
		# 脸框
		plt.gca().add_patch(plt.Rectangle(xy=(x,y),width=w, height=h,
								  edgecolor="red",fill=False, linewidth=1))
		# plt.gca().add_patch(plt.Rectangle(xy=(x,y-20),width=50, height=20,
								  # edgecolor="red",fc="red", linewidth=1))
		
		plt.text(x=x+1, y=y-1, s=str(age)+' / '+gender+' / '+str(beauty)+"'",fontdict=dict(fontsize=8, color='red'))
								  # bbox={'facecolor': 'red','edgecolor':'red','pad':1})
		plt.show()
		
		
		

## 构建一个类，用于读取文件夹内容。
class Dir():
	def __init__(self,path='.'):
		if path == '.':
			self.path = os.getcwd()
		else:
			self.path = path
		self.stuff = os.listdir(self.path)
		self.size = self.getdirsize(self.path)
		self.typedic = {'picture':'jpg.gif.jpeg.png.webp.jfif'.split('.'),'audio':'mp3.amr'.split('.'),'video':'mp4.rmvb.avi'.split('.'),'text':'txt.ini.xml'.split('.')}
		# self.helpbs = self.readhp()
		# self.hp = self.helpbs.help.string
		self.cash = self.p(r'cash\cash0')  # 缓存目录
	
	def cgo(self,path='.'):
		self.path = path
	
	def cg(self,cashpath):
		# 修改缓存目录
		self.cash = cashpath
	
	def father(self,floor):
		lever = os.path.split(self.path)
		if floor < len(lever):
			new_lever = lever[:len(lever)-floor]
			return '\\'.join(new_lever)
		else:
			new_lever = lever[0]
			return new_lever
	
	def rm(self,fname):
		os.remove(self.p(fname))
	
	def clear(self):
		# 清理缓存
		cash_name_list = os.listdir(self.cash)
		for i in range(len(cash_name_list)):
			cash_path = os.path.join(self.cash,cash_name_list[i])
			os.remove(cash_path)
			percent = int(((i+1)/len(cash_name_list)*100)/5)
			perc = '★'*percent+'☆'*(20-percent)
			print('\r清理缓存中<%d/%d>【%s】'%(i+1,len(cash_name_list),perc),end='')
		print('\n')
	
	def kill(self):
		# 清空文件夹
		files = self.get()[1]
		confirm = input('允许伦家大开杀戒吗？[Yes/any]')
		name_len = 0
		for i in files:
			if len(i) > name_len:
				name_len = len(i)
		if confirm == 'Yes':
			for i in range(len(files)):
				os.remove(self.p(files[i]))
				if len(files[i]) > 30:
					show = '...' + files[i][len(files[i])-30+3:]
				else:
					show = files[i] + ' '*(30-len(files[i]))
				print('\r已杀死['+ str(i+1) + '/' + str(len(files)) + ']'+ '【' + show + '】',end='')
	
	def p(self,filename):
		# 添加文件夹路径
		return os.path.join(self.path,filename)
	
	def op(self):
		os.startfile(self.path)
	
	def opc(self):
		os.startfile(self.cash)
	
	def get(self,path=''):
		# 【数据】获取文件夹内所有文件夹和文件名称
		if path == '':
			path = self.path
		alllist = os.listdir(path)
		dirlist = []
		filelist = []
		for f in alllist:  
			if(os.path.isdir(path + '/' + f)):  
				dirlist.append(f)  
			if(os.path.isfile(path + '/' + f)):
				filelist.append(f)
		return [dirlist,filelist]
	
	def getdirsize(self,dir):
		# 【数据】文件夹大小
		size = 0
		for root, dirs, files in os.walk(dir):
			size += sum([getsize(join(root, name)) for name in files])
		return size
	
	def filesize(self,filename):
		# 【数据】某文件大小
		return getsize(filename)
		
	# def readhp(self):
		# # 【功能】读取帮助文档
		# hasit = os.path.exists('DirClassHelp.xml')
		# if hasit:
			# with open('DirClassHelp.xml', 'r', encoding='utf-8') as f:
				# xml = bs(f.read(),'html.parser')
			# return xml
		# else:
			# print('嘤嘤嘤...找不到帮助文档...')
	
	'''文件夹操作'''
	def shdir(self,dirname,mode=''):
		# 【功能】搜索子文件夹
		i = 0
		result = []
		if mode == 'full':
			print('严厉搜索...')
		else:
			print('模糊搜索...')
		for root, lists, files in os.walk(self.path):
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
						print('%d %s' % (i, write))
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
				if ask == 'y':
					os.startfile(result[0])
	
	'''文件操作'''
	def ft(self):
		# 【数据】所有文件类型组成的列表
		fts = []
		for f in self.get()[1]:
			ftype = f.split('.')[-1]
			# print(ftype)
			fts.append(ftype)
		fts = list(set(fts))
		fts.sort()
		return fts
		
	def ftdic(self):
		# 【数据】各文件类型的文件数
		alllist = self.get()[1]
		ftlist = self.ft()
		ct = []
		n = 0
		for i in range(len(ftlist)):
			ct.append([])
		for t in ftlist:
			for f in alllist:
				if t in f.split('.')[-1]:
					n += 1
			ct[ftlist.index(t)].append(n)
			n = 0
		ft_dict = {}
		for i in range(len(ct)):
			ft_dict[ftlist[i]] = ct[i][0]
		# print(ft_dict)
		return ft_dict
	
	def id(self,file_path):
		# 【功能】获取文件的MD5值
		md5_1 = md5()  #创建一个md5算法对象
		with open(file_path,'rb') as f:  #打开一个文件，必须是'rb'模式打开
			md5_1.update(f.read())
		ret = md5_1.hexdigest()  #获取这个文件的MD5值
		return ret
	
	def cpdir(self,p1,p2):
		# 【功能】比较两个文件夹
		dir1 = Dir(p1)
		dir2 = Dir(p2)
		flist1 = dir1.get()[1]
		flist2 = dir2.get()[1]
		md1 = []
		md2 = []
		result = []
		for i in range(len(flist1)):
			f1 = os.path.join(dir1.path,flist1[i])
			md1.append(dir1.id(f1))
			if len(flist1[i]) > 30:
					show = '...' + flist1[i][len(flist1[i])-30+3:]
			else:
				show = flist1[i] + ' '*(30-len(flist1[i]))
			print('\rLoading['+ str(i+1) + '/' + str(len(flist1)) + ']:',show,'【',md1[i],'】',end='')
			# print('\rLoading['+ str(i+1) + '/' + str(len(flist1)) + ']:【',md1[i],'】',end='')
		print('\n')
		for i in range(len(flist2)):
			f2 = os.path.join(dir2.path,flist2[i])
			md2.append(dir2.id(f2))
			if len(flist2[i]) > 30:
				show = '...' + flist2[i][len(flist2[i])-30+3:]
			else:
				show = flist2[i] + ' '*(30-len(flist2[i]))
			print('\rLoading['+ str(i+1) + '/' + str(len(flist2)) + ']:',show,'【',md2[i],'】',end='')
			# print('\rLoading['+ str(i+1) + '/' + str(len(flist2)) + ']:【',md2[i],'】',end='')
		print('\n')
		for i in range(len(md1)):
			for j in range(len(md2)):
				if md1[i] == md2[j]:
					result.append([flist1[i],flist2[j]])
		
		return result
		
	def charge_dir(self,goal):
		# 【功能】将目标中不存在的文件注入目标
		it_has = self.cpdir(self.path,goal)  # 目标中已存在的文件
		name_changed = []
		pass_it = []  # 不需要搬运的文件
		for a_b in it_has:
			pass_it.append(a_b[0])
			if a_b[0] != a_b[1]:
				print('检测到已存在异名文件【%s】'%a_b)
				name_changed.append(a_b)
		confirm = input('是否更新目标文件夹的文件名称？[Yes/any]')
		if confirm == 'Yes':
			for i in range(len(name_changed)):
				os.rename(os.path.join(goal,name_changed[i][1]),os.path.join(goal,name_changed[i][0]))
				if len(name_changed[i][0]) > 30:
					show = '...' + name_changed[i][0][len(name_changed[i][0])-30+3:]
				else:
					show = name_changed[i][0] + ' '*(30-len(name_changed[i][0]))
				print('\rChanging['+ str(i+1) + '/' + str(len(name_changed)) + '] 【'+show+'】',end='')
		all_source = self.get()[1]
		confirm = input('\n即将对剩余的【%d】个文件进行搬运：[Yes/any]'%(len(all_source)-len(it_has)))
		if confirm == 'Yes':
			for i in range(len(all_source)):
				if all_source[i] not in pass_it:
					o_file = self.p(all_source[i])
					n_file = os.path.join(goal,all_source[i])
					copyfile(o_file,n_file)
					if len(all_source[i]) > 30:
						show = '...' + all_source[i][len(all_source[i])-30+3:]
					else:
						show = all_source[i] + ' '*(30-len(all_source[i]))
					print('\rNO.'+ str(i+1) + '/' + str(len(all_source)) + '【' + show + '】',end='')
	
	def setdir(self):
		# 【功能】文件夹自身去重
		mds = []
		double = []
		flist = self.get()[1]
		for i in range(len(flist)):
			itsmd = self.id(os.path.join(self.path,flist[i]))
			mds.append(itsmd)
			print('\rLoading['+ str(i+1) + '/' + str(len(flist)) + ']:','【',itsmd,'】',end='')
		if len(set(mds)) != len(mds):
			print('文件夹有重复文件')
			need = 1
		else:
			need = 0
		if need:
			for i in range(len(mds)):
				for j in range(i+1,len(mds)):
					if mds[i] == mds[j]:
						print(flist[i],'<---->',flist[j])
						double.append(os.path.join(self.path,flist[j]))
		print('\n'+'-'*50)
		print('即将删除一下内容：')
		for i in double:
			print(i)
		print('='*50)
		yes = input('[Y/any]')
		if yes == 'Y':
			for i in range(len(double)):
				os.remove(double[i])
				print('\r',i+1,'/',len(double),'Del >>',double[i])
	
	def shfile(self,filename,mode=''):
		# 【功能】搜索文件
		i = 0
		result = []
		if mode == 'full':
			print('严厉搜索...')
		else:
			print('模糊搜索...')
		for root, lists, files in os.walk(self.path):
			for file in files:
				if mode == 'full':
					if filename.lower() == file.lower():
						i = i + 1
						write = os.path.join(root, file)
						print('%d %s' % (i, write))
						result.append(write)
				else:
					if filename.lower() in file.lower():
						i = i + 1
						write = os.path.join(root, file)
						print('%d %s' % (i, write))
						result.append(write)
		ask = input('Open? [y/number/any]')
		if result:
			if len(result)>1:
				try:
					index = int(ask)
					os.system('start ' + result[index-1])
				except:
					if ask == 'y':
						os.system('start ' + result[0])
					else:
						pass
			else:
				if ask == 'y':
					os.system('start ' + result[0])
	
	def set_shortcut(self,filename,lnkname,iconname = ""):  # 如无需特别设置图标，则可去掉iconname参数
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
	
	def move(self,f_list,mode):
		# mode: 0-不作为 1-生成快捷方式 2-复制文件 3-剪切
		to = self.cash
		if f_list:
			for t in range(len(f_list)):
				percent = int(((t+1)/len(f_list)*100)/5)
				perc = '★'*percent+'☆'*(20-percent)
				print('\r<%d/%d>【%s】'%(t+1,len(f_list),perc),end='')
				oldpath = os.path.join(self.path,f_list[t])
				newpath = os.path.join(to,f_list[t])
				# print('\n')  # 补上进度条缺失的换行符
				if mode == 0:
					# print('%s>>>%s'%(oldpath,newpath))
					pass
				elif mode == 1:
					self.set_shortcut(oldpath,newpath)
				elif mode == 2:
					copyfile(oldpath,newpath)
				elif mode == 3:
					copyfile(oldpath,newpath)
					os.remove(oldpath)
			print('\n')  # 补上进度条缺失的换行符
	
	def drawpie(self,tag_groups,title=[]):
		# 【功能】绘制文件类型分布饼状图
		def randcolor(n=1):
			# 生成随机色
			colors = []
			for i in range(n):
				colors.append((random.random(),random.random(),random.random()))
			return colors
		import matplotlib as mpl
		import matplotlib.pyplot as plt
		import numpy as np
		# plt.ion()
		ct_dic = {}
			
		for g in tag_groups:
			for t in g:
				ct_dic[t] = len(self.andtag(t))
		
		# os.system('CLS')
		mpl.rcParams["font.sans-serif"] = ["SimHei"]
		mpl.rcParams["axes.unicode_minus"] = False
		parts = []
		partionnums = []
		for tg in tag_groups:
			parts = []
			partionnums = []
			for t in tg:
				parts.append(t+'\n('+str(ct_dic[t])+')')
				partionnums.append(ct_dic[t])
			colors = randcolor(len(tg))
			
			total = 0
			for i in partionnums:
				total += int(i)
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
			if title == []:
				plt.title('文件分布'+str(total))
			else:
				plt.title(title[tag_groups.index(tg)]+'['+str(total)+']')
		plt.show()
	
	# def op(self):
		# read_tool = {'picture':'C:\\quickstart\\tu.lnk','audio':'C:\\quickstart\\wyy.lnk','video':'C:\\quickstart\\qqv','text':'C:\\quickstart\\np.lnk'}
		# file_ed = file.split('.')[-1]
		# for k,v in self.typedic.items():
			# if file_ed in v:
				# filetype = k
		# os.system('start ' + read_tool[filetype] + ' ' + file)
	
	
	
	# 筛选功能
	def clean(self,types=[]):
		# 筛选指定类型的文件
		result = []
		if types != []:
			for f in self.get()[1]:
				filetype = f.split('.')[-1].lower()
				if filetype in types:
					result.append(f)
			return result
		else:
			return self.get()[1]
	
	def andtag(self,tags,other=[],do=0):
		# 交集筛选
		taglist = tags.strip().split('.')
		if other == []:
			f_list = self.clean()  # 资源包
		else:
			f_list = other
		c_list = []
		for tag in taglist:	#一个一个目标标签来
			for file_name in f_list:  # 遍历资源
				file_tag = file_name.split('.')  # 抽取资源文件的标签
				if tag in file_tag:  # 看看此文件是否在要求范围内
					c_list.append(file_name)
			f_list = c_list[:]  # 一轮筛选完之后，准备下一轮
			c_list = []
		
		self.move(f_list,do)
		return f_list
	
	def ortag(self,tags,other=[],do=0):
		# 并集筛选
		taglist = tags.strip().split('.')
		if other == []:
			f_list = self.clean()  # 资源包
		else:
			f_list = other
		c_list = []
		for tag in taglist:	#一个一个目标标签来
			for file_name in f_list:  # 遍历资源
				file_tag = file_name.split('.')  # 抽取资源文件的标签
				if tag in file_tag:  # 看看此文件是否在要求范围内
					c_list.append(file_name)
		f_list = c_list[:]
		
		self.move(f_list,do)
		return f_list
	
	def notag(self,tags,other=[],do=0):
		# 补集筛选
		taglist = tags.strip().split('.')
		if other == []:
			f_list = self.clean()  # 资源包
		else:
			f_list = other
		c_list = f_list[:]
		del_count = 0
		pass_count = 0
		note = [[],[]]  # [[删除的文件序号]，[保留的文件序号]]
		for tag in taglist:	#一个一个目标标签来
			# print('现在开始排除%s'%tag)
			record1 = []
			record2 = []
			for file_name in f_list:  # 遍历文件
				file_tag = file_name.split('.')  # 抽取文件的标签
				if tag in file_tag:  # 不符合要求
					del_count += 1
					# print('\r检测标签【%s】>>删除%d<<当前剩余文件：【%d】'%(tag,del_count,len(f_list)),end='')
					record1.append(file_name.split('.')[-2])
					try:
						c_list.remove(file_name)  # 把她踢了
					except Exception as e:
						# print(e)
						print('【',file_name,'】不在列表中')
				else:
					# print('文件【%s】的标签有'%file_name,file_tag,'标签【%s】不在其中'%tag)
					pass_count += 1
					# print('\r检测标签【%s】>>跳过%d<<当前剩余文件：【%d】'%(tag,pass_count,len(f_list)),end='')
					record2.append(file_name.split('.')[-2])
					continue
				# print('\n')
				
			note[0].append(record1)
			note[1].append(record2)
		f_list = c_list[:]
			
		print('\n')
		# print('NOTE:\n',note)
		self.move(f_list,do)
		return f_list
		
		
	
	def insize(self,s,type='picture',other=[],m='=',do=0):
		if other == []:
			filelist = self.clean(self.typedic[type])
		else:
			filelist = other
		# print(filelist)
		f_list = []
		if s[-1] == 'k':
			ss = int(s[:-1]) * 1024
		elif s[-1] == 'm':
			ss = int(s[:-1]) * 1024 * 1024
		for i in range(len(filelist)):
			size = self.filesize(self.p(filelist[i]))
			if m == '=':
				if size == ss:
					f_list.append(filelist[i])
			elif m == '>':
				if size >= ss:
					f_list.append(filelist[i])
			elif m == '<':
				if size <= ss:
					f_list.append(filelist[i])
		self.move(f_list,do)
		return f_list

	def format_name(self):
		# 文件名编号
		f_list = self.clean()
		old_names = []
		useful = []  # 文件名是否有用
		used_num = []  # 已经使用过的数字
		for i in range(len(f_list)):
			oldname = f_list[i].split('.')[-2]
			old_names.append(oldname)
		for i in range(len(old_names)):
			try:
				num = int(old_names[i])  # 名字是数字
				if num > len(old_names):
					# 无用数字名
					# print('【%d】无用数字名'%num)
					useful.append(0)
				else:
					# 有用数字名，不用修改
					if num not in used_num:
						# 该有用数字还没被用过
						useful.append(1)
						used_num.append(num)
					else:
						# 她已经被用过了
						# print('【%d】她已经被用过了'%num)
						useful.append(0)
			except:
				# 文件名不是数字
				# print('【%s】不是数字'%old_names[i])
				useful.append(0)
				
		print(useful)
		for i in range(len(old_names)):
			if not useful[i]:
				for j in range(1,len(f_list)+1):
					if j not in used_num:
						new_num = j
						used_num.append(new_num)
						print('添加编号【%d】'%j)
						break
				new_fname = '.'.join(f_list[i].split('.')[:-2]) + '.' + str(new_num) + '.' + f_list[i].split('.')[-1]
				os.rename(os.path.join(self.path,f_list[i]),os.path.join(self.path,new_fname))
				# print("%d【%s】>>>【%s】"%(i,os.path.join(self.path,f_list[i]),new_fname))
 

#### 测试

# def preee():
	# pics = Dir('D:\\#My\\GiData\\Source\\Arts\\Images')
	# dirs = pics.get()[0]
	# for i in range(len(dirs)):
		# print('%d\t%s'%(i,dirs[i]))
	# try:
		# num = int(input('序号：'))
	# except:
		# num = 8
	
	# dir = Dir(os.path.join(pics.path,dirs[num]))
	# print('文件夹为【%s】'%dirs[num])
	# print('初始化图片：%s'%dir.get()[1][0])
	# img = Pic(os.path.join(dir.path,dir.get()[1][0]))
	# img.preview(dir.andtag('打斗'))
	
# def ssort():
	# pics = Dir('D:\\#My\\GiData\\Source\\Arts\\Images')
	# dirs = pics.get()[0]
	# for i in range(len(dirs)):
		# print('%d\t%s'%(i,dirs[i]))
	# try:
		# num = int(input('序号：'))
	# except:
		# num = 8
	
	# dir = Dir(os.path.join(pics.path,dirs[num]))
	# print('文件夹为【%s】'%dirs[num])
	# print('初始化图片：%s'%dir.get()[1][0])
	# dir.format_name()

def tag_sys():
	root = Dir(r'D:\#My\GiData\Source\Arts\Images')  # 所有图片所在的根目录
	all_dirs = root.get()[0]  # 全部图片文件夹
	o_path = root.p(all_dirs[8])  # 源文件夹
	cash_dir = Dir(os.path.join(o_path,r'TAGW\cash'))  # 缓存文件夹
	cashs = []
	for i in cash_dir.get()[0]:
		cashs.append(cash_dir.p(i))
	view_path = cashs[0]  # 最终的浏览文件夹
	here = Dir(o_path)
	here.cgcash(view_path)
	print('当前位置：',o_path)
	print('缓存目录：',view_path)
	
	tag_txt = input('请输入标签↓\n>>>').strip()
	mode = input('模式：')
	while mode != 'q':
		md = mode.split(' ')
		try:
			if mode == 'cg':
				print('请选择缓存目录：')
				for i in range(len(cashs)):
					print('%d\t%s'%(i,cashs[i]))
				c = input('缓存目录改为：')
				try:
					res = int(c)
					if res in range(len(cashs)):
						view_path = cashs[res]
					here.cgcash(view_path)
				except Exception as e:
					print(e)
					
			elif mode == 'cgo':
				print('请选择源目录：')
				for i in range(1,len(all_dirs)):
					if root.p(all_dirs[i]).split('\\')[-2] == 'Images':
						print('%d\t%s'%(i,all_dirs[i]))
				print('p\tD:\\#My\\GiData\\Daily\\photos')
				c = input('源目录改为：')
				try:
					res = int(c)
					if res in range(len(all_dirs)):
						o_path = root.p(all_dirs[res])
					else:
						o_path = root.p(all_dirs[8])
				except:
					if c == 'p':
						o_path = r'D:\#My\GiData\Daily\photos'
					else:
						o_path = root.p(all_dirs[8])
				here = Dir(o_path)
			
			elif md[0] == 'size':
				filelist = here.clean(here.typedic['picture'])
				# print(filelist)
				if len(md) == 1:
					s = tag_txt
					r = here.insize(s,m='>')
					# print(len(r))
				elif len(md) > 2:
					# 'size + >'
					s = tag_txt.split(' ')[0]
					try:
						t = tag_txt.split(' ')[1]
						if md[1] == '+':
							filelist = here.andtag(t)
						elif md[1] == '-':
							filelist = here.notag(t)
						elif md[1] == '/':
							filelist = here.ortag(t)
					except:
						# 没有指定标签要求
						pass
					
					if md[-1] == 'do':
						r = here.insize(s,m=md[2])
						os.startfile(view_path)
					else:
						r = here.insize(s,m=md[2])
					print(len(r))
			
		except Exception as e:
			print(e)
		print('\n'*2)
		print('#'*50)
		print('当前位置：',o_path)
		print('缓存目录：',view_path)
		tag_txt = input('请输入标签↓\n>>>').strip()
		mode = input('模式：')

if __name__ == '__main__':
	
	# tag_sys()
	
	# dir = Dir('D:\\#My\\GiData\\Source\\Arts\\Images\\Pics')
	# result = dir.charge_dir(r'E:\Gidata\Source\Arts\Images\pic')
	# result = dir.charge_dir('D:\\#My\\GiData\\Source\\Arts\\Images\\Pics')
	
	# dir = Dir(r'E:\Gidata\Source\Arts\Images\pic')
	# flist = dir.andtag('[gif]')
	# for i in flist:
		# print(i)
		# os.remove(dir.p(i))
	
	dir = Dir(r'D:\#My\GiData\Creation\Projects\Python\Gina\GiFun\GMain\tts_logs')
	md1 = dir.id(dir.p('[Chat]20210520222749.mp3'))
	md2 = dir.id(dir.p('[Chat]20210520222759.mp3'))
	print(md1)
	print(md2)