import pygame
from pygame.locals import *
import sys
from PIL import Image


'''参数设置'''
'''==============================='''
# pngsum = 24 #图片序列数量
pngsum = 180
picsquences = 'AIwave-{}.png'
# picsquences = 'C:\\Users\\111\\Documents\\桌面文件\\临时\\a\\img_{}.jpg'
fps = 50
title = "Show Gifs"
'''==============================='''

# 初始化pygame
pygame.init()
# 设置屏幕宽高
sw, sh = 300,180
ll = picsquences.split('{}')
getpic = ll[0]+'0'+ll[1]
img = Image.open(getpic)
print(img.size) #获取图片像素信息

picw,pich = img.size
picrate = picw/pich
if picw > pich:
	newpicw = int(sw)
	newpich = int(newpicw/picrate)
else:
	newpich = int(sh)
	newpicw = int(newpich*picrate)

size = (sw,sh)

# size = img.size #窗口适合图片尺寸
screen = pygame.display.set_mode(size,NOFRAME)
# 设置屏幕标题
pygame.display.set_caption(title)
clock = pygame.time.Clock()
# black = 0, 0, 0

listpng = [pygame.image.load(picsquences.format(i)).convert_alpha() for i in range(pngsum)]
print(len(listpng))
indexpng = 0
while True:
	for event in pygame.event.get():
		if (event.type == QUIT) or ((event.type == KEYDOWN) and (event.key == K_F12)):
			pygame.quit()
			sys.exit()
	showfsur = pygame.transform.scale(listpng[indexpng % len(listpng)],(newpicw,newpich))
	screen.blit(showfsur, (0,0))
	indexpng += 1 
	pygame.display.update()
	clock.tick(fps)#参数为频率，一般设30。越大越快