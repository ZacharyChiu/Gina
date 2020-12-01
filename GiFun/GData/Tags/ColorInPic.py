import sys, pygame, os
import win32com.client 
from pygame.locals import *
def keyPressed(inputKey): 
	#组合键支持函数
	keysPressed = pygame.key.get_pressed()
	if keysPressed[inputKey]:return True
	else:return False

def clean(l):
	img = ['jpg','jpeg','png','gif']
	new = []
	for i in l:
		if '.' in i:
			type = i.split('.')[-1]
		else:
			type = ''
		if type in img:
			new.append(i)
	return new

pygame.init()
side_lenth = 450
size = win_w, win_h = side_lenth, int(side_lenth*4/3)
sp = 3  # 拆分列数
screen = pygame.display.set_mode(size, pygame.RESIZABLE, 32)
# screen = pygame.display.set_mode(size,0, 32)
icon = pygame.image.load('D:\\#My\\GiData\\Creation\\Designs\\Pictures\\素材\\LogoD200322-Gina.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('GiPic')

scroll_length = 0
scroll_step = 100

class PicBar():
	def __init__(self,base,aalilh,n_w):
		## 初始化 ##
		self.color_size = (50,50)
		self.left_blank = 10
		self.between_blank = 10
		self.middle_blank = 10
		self.color_width = 50
		
		self.sur = []  # 所有surface对象。结构：[[主图一，色1，色2，……],[主图二，色1，色2，……], ...]
		self.ratos = []
		self.hs = []
		self.base = base
		self.aalilh = aalilh
		self.w = n_w  # 指定主图显示宽度
		self.pos = []
		
		self.load()
		self.place()
		
	def load(self):
		for hang in self.aalilh:  # 每一行
			sur0 = pygame.image.load(hang[0])  # 原图的surface对象
			o_size = sur0.get_rect()[2:]
			rato = sur0.get_rect()[2]/sur0.get_rect()[3]
			self.ratos.append(rato)
			n_h = int(self.w/rato)
			self.hs.append(n_h)  # 获得每张主图的高度
			sur0 = pygame.transform.scale(sur0,(self.w,n_h))  # 缩放主图到指定大小
			sur_hang = [sur0]
			for p in hang[1:]:
				sur1 = pygame.image.load(p)
				sur1 = pygame.transform.scale(sur1,self.color_size)
				sur_hang.append(sur1)
			self.sur.append(sur_hang)  # 所有surface对象收集完毕
				
	def place(self):
		a = [self.left_blank,10]
		ba = [a[0]+self.w+self.middle_blank,10]
		bb = [a[0]+self.w+self.middle_blank*2+self.color_width]
		self.pos.append([a,ba])
		
		for i in range(1,len(self.sur)):  # 第i+1层对象
			h_above = 10
			for j in range(i):
				h_above = h_above + self.hs[j]
			y = h_above + self.between_blank*(j+1)
			a = [10,y]
			ab = [a[0]+self.w+self.middle_blank,y]
			self.pos.append([a,ab])
		
		self.long = self.pos[-1][0][1] + self.hs[-1]
	
	def update_w(self,w):
		self.w = w
		self.load()
		self.place()

	def blit(self,scroll=0):
		for i in range(len(self.sur)):
			for j in range(len(self.sur[i])):
				self.base.blit(self.sur[i][j],(self.pos[i][j][0],self.pos[i][j][1]+scroll))
		self.scroll = scroll
	def msin(self,scroll):
		# mouse in。判断鼠标是否进入按钮所在区域
		ms_x, ms_y = pygame.mouse.get_pos()
		print('\r鼠标高度：',ms_y,' ',end='')

		lie = 0
		choice = ''

		if ms_x >= self.left_blank and ms_x <= self.left_blank + self.w:
			for i in range(len(self.pos)):  # h = [a,ab]
				pic_y0 = self.pos[i][0][1] + scroll
				pic_y1 = pic_y0 + self.hs[i]
				if ms_y >= pic_y0 and ms_y <= pic_y1:
					print('识别到鼠标位于【',i,'】')
					choice = self.aalilh[i][0]
					break
					
		return choice
		



## 构建总图集列表aalilh ##	
aalilh = []
color_path = 'D:\\#My\\GiData\\Creation\\Projects\\Python\\Gina\\GiFun\\GData\\Color'
color_list = clean(os.listdir(color_path + '\\唇色'))
color_i = []  # 已经提取过颜色的图片的序号集合
for c in color_list:
	color_i.append(c.split('@')[0])

all_pic_list = clean(os.listdir('..'))
pic_list = []  # 提取过颜色的图片（文件名）集合
for i in color_i:
	for p in all_pic_list:
		if '.'+i+'.' in p:
			pic_list.append('..\\'+p)

for i in range(len(pic_list)):
	aalilh.append([pic_list[i],color_path+'\\唇色\\'+color_list[i]])

# print('#aalilh#')
# for i in aalilh:
	# print(aalilh.index(i),'|',i)

bar_rate = 4/7
bar_w = int(win_w*bar_rate)
bar = PicBar(screen,aalilh,bar_w)	
# for i in range(len(bar.pos)):
	# print('POS[Y]:',bar.pos[i][0][1],'||',bar.hs[i])
while 1:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		
		if event.type == VIDEORESIZE:
			SCREEN_SIZE = event.size
			screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
			bar.update_w(int(SCREEN_SIZE[0]*bar_rate))
			size = win_w, win_h = SCREEN_SIZE[0], SCREEN_SIZE[1]
			
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			pressed_array = pygame.mouse.get_pressed()
			if event.button == 4:
				if scroll_length < 0:
					scroll_length += scroll_step
				else:
					scroll_length = 0
			elif event.button == 5:
				if scroll_length > -1*(bar.long+scroll_length-win_h):	
					scroll_length -= scroll_step
			elif pressed_array == (1,0,0):
				# 点击鼠标左键
				print('scroll:',scroll_length)
				try:
					os.system('start '+bar.msin(scroll_length))
				except:
					print('打不开。')
			
	screen.fill((40,40,40))
	bar.blit(scroll_length)
	pygame.display.update()
	