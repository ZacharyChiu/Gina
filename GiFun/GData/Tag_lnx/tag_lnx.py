# -*- coding = utf-8 -*-
# Author: Zachary

from bs4 import BeautifulSoup
import os

class Tags():
	def __init__(self,pic_path):
		self.op = pic_path
		self.opc = os.path.join(os.getcwd(),'cash','cash0')
		
		with open('tag.conf','r',encoding='utf-8') as f:
			text = f.read()
		self.conf = BeautifulSoup(text,'html.parser')  # 加载配置文件


	def conft(self,element):
		# 方便读取配置文件的内容
		return eval('self.conf.' + element + '.string.strip()')

		
	def help(self,content='hp'):
		return eval("self.conft('help." + content + "')")


	def write_result(path,filelist):
		# 把筛选结果保存为文本
		with open(path,'w',encoding='utf-8') as f:
			f.write('\n'.join(filelist))
			
			
	def mklnk(self,opath,npath):
		# 创建快捷方式
		os.system('ln -s ' + opath + ' ' + npath)	
	
	
	def cleardir(self,path):
		flist = os.listdir(path)
		for f in flist:
			os.system('rm -r ' + os.path.join(path,f))
	
		
			
	def clean(self,l):
		# 将不符合条件的文件类型剔除
		new = []
		for i in l:
			if '.' in i:
				type = i.split('.')[-1]
			else:
				type = ''
			if type in self.ft:
				new.append(i)
		return new
	
	
	def load(self):
		# 运行,使得一些不方便在初始化中的操作得以实施
		self.ft = self.conft('ft').split('.')  # []所有文件类型
		self.filelist = self.clean(os.listdir(self.op))  # []所有文件
		alltag = []
		for f in self.filelist:
			filetag = f.split('.')[:-2]
			for t in filetag:
				if t not in alltag:
					alltag.append(t)
		self.at = alltag  # []所有出现过的标签
		
		
	def andmode(self,tag_order):
		tago = tag_order.split('.')  # 筛选条件集合
		flist = self.filelist[:]
		clist = []
		for tag in tago:
			for filename in flist:
				filetag = filename.split('.')
				if tag in filetag:
					clist.append(filename)
			flist = clist[:]
			clist = []
		return flist
		
		
	def notmode(self,tag_order):
		def round_(tag,flist):
			for filename in flist:
				filetag = filename.split('.')
				if tag in filetag:
					flist.remove(filename)
					round_(tag,flist)
		
		tago = tag_order.split('.')  # 筛选条件集合
		flist = self.filelist[:]
		for tag in tago:
			round_(tag,flist)  # 使用递归算法
		return flist
		
		
	def ormode(self,tag_order):
		tago = tag_order.split('.')
		flist = self.filelist[:]
		clist = []
		for tag in tago:
			for filename in flist:
				filetag = filename.split('.')
				if tag in filetag:
					clist.append(filename)
		flist = clist[:]
		return flist


def main():
	pics = Tags(os.getcwd() + '/data')
	pics.load()
	print('Path:',pics.op)
	print('Cash:',pics.opc)
	tag_order = input('[ Order ]\n>>> ')
	mode = input('Mode: ')
	while mode != 'q':
		try:
			md = mode.split(' ')
			if md[0] == '+':
				result = pics.andmode(tag_order)
				if len(md) == 1:
					# 默认执行模式: 将结果放到缓存文件夹中
					pics.cleardir(pics.opc+'/')
					for p in result:
						pics.mklnk(pics.op+'/'+p,pics.opc+'/'+p+'.ln')
					# os.system('nautilus ' + pics.opc)
				else:
					if md[1] == 's':
						# show, 显示结果
						print('='*10+'RESULT:'+str(len(result))+'='*10)
						print('\n'.join(result))
					elif md[1] == 'c':
						# count, 统计数量
						print('RESULT:[ %d ]'%len(result))
						
			elif md[0] == '-':
				result = pics.notmode(tag_order)
				if len(md) == 1:
					# 默认执行模式: 将结果放到缓存文件夹中
					pics.cleardir(pics.opc+'/')
					for p in result:
						pics.mklnk(pics.op+'/'+p,pics.opc+'/'+p+'.ln')
				else:
					if md[1] == 's':
						# show, 显示结果
						print('='*10+'RESULT:'+str(len(result))+'='*10)
						print('\n'.join(result))
					elif md[1] == 'c':
						# count, 统计数量
						print('RESULT:[ %d ]'%len(result))
			elif md[0] == '/':
				result = pics.ormode(tag_order)
				if len(md) == 1:
					# 默认执行模式: 将结果放到缓存文件夹中
					pics.cleardir(pics.opc+'/')
					for p in result:
						pics.mklnk(pics.op+'/'+p,pics.opc+'/'+p+'.ln')
				else:
					if md[1] == 's':
						# show, 显示结果
						print('='*10+'RESULT:'+str(len(result))+'='*10)
						print('\n'.join(result))
					elif md[1] == 'c':
						# count, 统计数量
						print('RESULT:[ %d ]'%len(result))
		except Exception as e:
			print(e.args)
		
		print('\n'*2)	
		print('Path:',pics.op)
		print('Cash:',pics.opc)
		tag_order = input('[ Order ]\n>>> ')
		mode = input('Mode: ')
	# pics.cleardir(pics.opc+'/')
	# for p in re:
		# pics.mklnk(pics.op+'/'+p,pics.opc+'/'+p+'.ln')
	# print('\n'.join(pics.notmode('anqr.iahx')))
	
	
if __name__ == '__main__':
	main()
