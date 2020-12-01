import pygame
from pygame.locals import *
import os
from PIL import Image
from shutil import copyfile

def clean(l):
	file_type = 'jpg.png.webp.gif.jpeg.jfif'
	img = file_type.split('.')
	new = []
	for i in l:
		if '.' in i:
			ftype = i.split('.')[-1]
		else:
			ftype = ''
		if ftype.lower() in img:
			new.append(i)
	return new

def analyseImage(path):
    '''
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode
    before processing all frames.
    预处理通过图像来确定模式(全模式或加法模式)。
    必要的，因为评估单个框架是不可靠的。需要知道模式
    在处理所有帧之前。
    '''
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

def processImage(path):
    '''
    Iterate the GIF, extracting each frame.
    '''
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
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            如果GIF使用本地颜色表，每个框架都有自己的调色板。
            如果没有，我们需要将全局调色板应用到新框架上。
            '''
            if not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)

            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            这个文件是一个“部分”模式的GIF，其中帧更新一个不同大小的区域到整个图像?
            如果是这样，我们需要通过将新框架粘贴到前面的框架上来构建新框架。
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(im, (0, 0), im.convert('RGBA'))
            #存储到gif所在目录
            new_frame.save('%s-%d.png' % (''.join(path.split('.')[:-1]), i), 'PNG')

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass


def keyPressed(inputKey): 
    #组合键支持函数
    keysPressed = pygame.key.get_pressed()
    if keysPressed[inputKey]:return True
    else:return False

s_path = os.getcwd()
f_list = clean(os.listdir(s_path))	#获取源文件夹内所有文件名
print('#'*50)
for i in f_list:
	print(i)
print('#'*50)
sw, sh = 800,600

#初始化
pygame.init()
screen = pygame.display.set_mode((sw,sh),0,32)
pygame.display.set_caption('显示图片')

findex = 0
next = 0
prev = 0
noframe = 0
fullscreen = 0
moving = 0
cashpath = os.getcwd()
giflist = clean(os.listdir(cashpath))
splitit = 1
while True:
	showfname = s_path + '\\' + f_list[findex]
	
	if showfname[-3:] == 'gif':
		print('这他妈是动态图')
		# if splitit:
			# copyfile(showfname,cashpath+'\\'+f_list[findex])
			# processImage(cashpath+'\\'+f_list[findex])
			# giflist = os.listdir(cashpath)
			# os.remove(cashpath+'\\'+f_list[findex])
			# splitit = 0
			
		# 
	else:
		showfsur = pygame.image.load(showfname)
		picw = showfsur.get_width()
		pich = showfsur.get_height()
		picrate = picw/pich
		if picw > pich:
			newpicw = int(sw)
			newpich = int(newpicw/picrate)
		else:
			newpich = int(sh)
			newpicw = int(newpich*picrate)
		showfsur = pygame.transform.scale(showfsur,(newpicw,newpich))
		
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		if event.type == KEYDOWN:
			if keyPressed(K_ESCAPE):
				exit()
			if keyPressed(K_TAB):
				noframe = not noframe
			if keyPressed(K_F12):
				fullscreen = not fullscreen
			
			if keyPressed(K_RIGHT):
				print('next pic')
				next = 1
			if keyPressed(K_LEFT):
				print('previous pic')
				prev = 1
			
		if event.type == KEYUP:
			if event.key == K_RIGHT:
				next = 0
			if event.key == K_LEFT:
				prev = 0
		if event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				moving = not moving
	
		#开关执行
		if noframe:
			screen = pygame.display.set_mode((sw,sh),NOFRAME,32)
		elif fullscreen:
			screen = pygame.display.set_mode((sw,sh),FULLSCREEN,32)
		else:
			screen = pygame.display.set_mode((sw,sh),0,32)
			
		if next:
			if findex < len(f_list)-1:
				findex += 1
			else:
				findex = 0
		if prev:
			if findex == 0:
				findex = len(f_list)-1
			else:
				findex -= 1
		if moving:
			mx,my = pygame.mouse.get_pos()
			picx = mx - newpicw/2
			picy = my - newpich/2
			
		else:
			picx = sw/2 - newpicw/2
			picy = sh/2 - newpich/2
		
	
	screen.fill((50,50,50))
	#显示图片
	screen.blit(showfsur,(picx,picy))
	pygame.display.update()