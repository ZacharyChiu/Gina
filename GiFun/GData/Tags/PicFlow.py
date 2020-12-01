import sys, pygame, os
import win32com.client 
from pygame.locals import *
def keyPressed(inputKey): 
	#组合键支持函数
	keysPressed = pygame.key.get_pressed()
	if keysPressed[inputKey]:return True
	else:return False

pygame.init()
size = win_w, win_h = 1200, int(1200*9/16)
sp = 3  # 拆分列数
# screen = pygame.display.set_mode(size, pygame.RESIZABLE, 32)
screen = pygame.display.set_mode(size,0, 32)
icon = pygame.image.load('D:\\#My\\GiData\\Creation\\Designs\\Pictures\\素材\\LogoD200322-Gina.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('GiPic')

scroll_length = 0
scroll_step = 100

class PicBar():
	def __init__(self,base,pics,n_w):
		## 初始化 ##
		self.ku = []
		self.o_sizes = []
		self.ratos = []
		self.hs = []
		self.base = base
		self.pics = pics
		self.w = n_w
		
	def load(self):
		for p in self.pics:
			self.ass = pygame.image.load(p) # 最终，ass将成为图库的最后一张图的surface对象
			o_size = self.ass.get_rect()[2:]
			rato = self.ass.get_rect()[2]/self.ass.get_rect()[3]
			self.o_sizes.append(o_size)
			self.ratos.append(rato)
			n_h = int(self.w/rato)
			self.hs.append(n_h)
			self.ass = pygame.transform.scale(self.ass,(self.w,n_h))
			self.ku.append(self.ass)# ku是当前图集surface对象库（列表）
	def add(self,new_pics):
		for p in new_pics:
			try:
				self.ass = pygame.image.load(p) # 最终，ass将成为图库的最后一张图的surface对象
				o_size = self.ass.get_rect()[2:]
				rato = self.ass.get_rect()[2]/self.ass.get_rect()[3]
				self.o_sizes.append(o_size)
				self.ratos.append(rato)
				self.pics.append(p)
				n_h = int(self.w/rato)
				self.hs.append(n_h)
				self.ass = pygame.transform.scale(self.ass,(self.w,n_h))
				if self.ass not in self.ku:
					self.ku.append(self.ass)# ku是当前图集surface对象库（列表）
			except:
				print(p,'加载不了。')
	def place(self,winsize):
		pos = []
		ceng = []
		three = self.hs[:sp]
		print('Three',three)
		for sur in self.ku:
			if self.ku.index(sur) == 0:
				pos.append([5,0])
			elif self.ku.index(sur) < sp:
				i = self.ku.index(sur)
				x = 5*(i+1)+int((winsize[0]-5*4)/sp)*i
				y = 0
				pos.append([x,y])
			else:
				loc = three.index(min(three))
				x = 5*(loc+1)+int((winsize[0]-5*4)/sp)*loc
				y = three[loc]+5
				pos.append([x,y])
				three[loc] = three[loc] + self.hs[self.ku.index(sur)]
				if loc == 0:
					three[1] += 5
					three[2] += 5
				elif loc == 1:
					three[0] += 5
					three[2] += 5
				elif loc == 2:
					three[1] += 5
					three[0] += 5
		
		for n in range(len(pos)):
			a = pos[n][1]
			b = pos[n][1] + self.hs[n]
			l = pos[n][0]
			if l >= 5:
				if l <= 5 + self.w:
					lie = 1
				elif l >= 5*2 + self.w:
					if l <= 5*2 + self.w*2:
						lie = 2
					elif l >= 5*sp +self.w*2:
						if l <= 5*sp +self.w*sp:
							lie = sp
			ceng.append([a,b,lie])
			
		self.buttom = max(three) # 排列后的最低线高度
		self.pos = pos
		self.ceng = ceng
		

	def blit(self,n,x,y):
		self.base.blit(self.ku[n],(x,y))
	def msin(self,scroll):
		# mouse in。判断鼠标是否进入按钮所在区域
		ms_x, ms_y = pygame.mouse.get_pos()
		ms_h = ms_y-scroll

		# print('图片高度集：',self.hs)
		# print('\r鼠标高度：',ms_h,' ',end='')
		hang = []
		lie = 0

		for i in range(0,len(self.hs),sp):
			# print(i)
			hang.append(self.pos[i:i+sp])
		# print(hang,end='')
		choice = -1
		if ms_x >= 5:
			if ms_x <= 5 + self.w:
				lie = 1
			elif ms_x >= 5*2 + self.w:
				if ms_x <= 5*2 + self.w*2:
					lie = 2
				elif ms_x >= 5*sp +self.w*2:
					if ms_x <= 5*sp +self.w*sp:
						lie = sp
		for c in self.ceng:
			if ms_h >= c[0] and ms_h <= c[1]:
				if lie == c[-1]:
					choice = self.ceng.index(c)
		return bars.pics[choice]
		



## 路径 ##	
# path = 'D:\\#My\\GiData\\Source\\Arts\\Images\\Pics'
# aalilh = os.listdir(path)
# for i in range(len(aalilh)):
	# aalilh[i] = path + '\\' + aalilh[i]
path = 'cash\\cash0'
aalilh = []
img_type = ['jpg','jpeg','png','gif']
goal = os.listdir(path)
choose = {}

links = []
for img in goal:
	if img.split('.')[-2] in img_type:
		links.append(img)
		# print(img)
for lnk in links:
	pre = ''
	shell = win32com.client.Dispatch("WScript.Shell")
	lnkpath = path+'\\'+lnk
	choose[lnkpath] = 0
	
	shortcut = shell.CreateShortCut(lnkpath)
	target = shortcut.Targetpath
	# print(target)
	aalilh.append(target)
# print('CHOOSE:\n',choose)

## 实例化
# print(aalilh)
num = 6
bar_w = int((win_w-5*4)/sp)
bars = PicBar(screen,aalilh[0:num],bar_w)
bars.load()
bars.place(size)
# print('POS:',bars.pos)
ass = 0

## 主循环
while 1:
	# msp = pygame.mouse.get_pos()
	# print('mouse:',ms_pos)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == KEYDOWN:
			if keyPressed(K_F1):
				sp += 1
				bar_w = int((win_w-5*4)/sp)
				bars = PicBar(screen,aalilh[0:num],bar_w)
			if keyPressed(K_F12):
				to_del = []
				to_keep = []
				for k,v in choose.items():
					if v == True:
						to_keep.append(k)
					else:
						to_del.append(k)
				print('保留文件：\n')
				for f in to_keep:
					print('【',f,'】')
				yes = input('#########是否确认删除#########\n')
				if yes == 'yes':
					for f in to_del:
						os.remove(f)
						print('>>>删除：',f)
				else:
					print('已取消')
		if event.type == pygame.MOUSEBUTTONDOWN:
			pressed_array = pygame.mouse.get_pressed()
			if pressed_array == (1,0,0):
				# 元组各个数字代表鼠标左中右键
				in_it = bars.msin(scroll_length)
				os.system('start '+in_it)
			# if pressed_array == (0,0,1):
				# # in_it就是源文件名
				# in_it = bars.msin(scroll_length)
				# click = in_it.split('\\')[-1]+'.lnk'
				# name = in_it.split('\\')[-1].split('.')[-2]
				# print('【',name,'】')
				# choose[path+'\\'+click] =  not choose[path+'\\'+click]
				# io = []
				# for k,v in choose.items():
					# io.append(v)
				# print(io)
			if pressed_array == (0,0,1):
				in_it = bars.msin(scroll_length)
				print('Index【'+in_it.split('.')[-2]+'】')
			if event.button == 4:
				if scroll_length < 0:
					scroll_length += scroll_step
				else:
					scroll_length = 0
			elif event.button == 5:
				if scroll_length > -1*(bars.buttom-win_h):	
					scroll_length -= scroll_step

				
				
			# print('\r位置：',scroll_length,'    ',end='')
	screen.fill((40,40,40))
	# print('底线：',bars.buttom+scroll_length)
	if bars.buttom+scroll_length < win_h and num+6 < len(aalilh):
		print('adding...')
		num += 6
		bars.add(aalilh[num:num+6])
		bars.place(size)
	for i in range(len(bars.ku)):
		bars.blit(i,bars.pos[i][0],bars.pos[i][1]+scroll_length)
	# print('库长',len(bars.ku))
	# print('\rPOS:',bars.pos,end='')
	pygame.display.update()