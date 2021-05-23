from gdata import Dir
import os
from win32com.shell import shell
from win32com.shell import shellcon
import win32com.client 

def modes(order):
	pass

pic = Dir(r'D:\#My\GiData\Source\Arts\Images\Pics')  # 实例化

pic.cg(pic.p(r'TAGW\cash\cash0'))

# print('TESTTTTT:')
# print(pic.father(1))

# 打印基本信息
print('当前位置：'+pic.path)
print('缓存目录：',pic.cash)

# 用户输入
tags = input('请输入标签↓\n>>>').strip()
mode = input('模式：')

while mode != 'q':  # 主循环
	md = mode.split('.')
	if md[0] == 're':
		print('='*50)
		os.system(r'python D:\#My\GiData\Creation\Projects\Python\Gina\GiFun\GData\test_gidata.py')
	# 基本文件夹操作
	elif md[0] == 'cg':
		# 改缓存目录
		# cash_dir = Dir(pic.p(os.path.join('TAGW','cash')))
		dir_list = pic.get(path=pic.p(os.path.join('TAGW','cash')))[0]
		for i in range(len(dir_list)):
			print('%d\t%s'%(i,dir_list[i]))
		choice = input('Choice: ')
		pic.cg(os.path.join(pic.p(os.path.join('TAGW','cash')),dir_list[int(choice)]))
	
	elif md[0] == 'cgo':
		# 改资源目录
		o_dir = r'D:\#My\GiData\Source\Arts\Images'
		dir_list = pic.get(path=r'D:\#My\GiData\Source\Arts\Images')[0]
		for i in range(len(dir_list)):
			print('%d\t%s'%(i,dir_list[i]))
		print('p\tD:\#My\GiData\Daily\photos')
		choice = input('Choice: ')
		if choice == 'p':
			pic = Dir('D:\#My\GiData\Daily\photos')
		else:
			try:
				pic = Dir(os.path.join(o_dir,dir_list[int(choice)]))
			except Exception as e:
				print(e)
				print('有内鬼，终止交易！')
	
	elif md[0] == 'op':
		# 打开资源
		pic.op()
	elif md[0] == 'opc':
		# 打开缓存文件夹
		pic.opc()
	
	# 筛选系统
	elif md[0] == 'all':
		pic.clear()
		pic.move(pic.get()[1],mode=1)
		pic.opc()
	elif md[0] == '+':
		if len(md) == 1:
			pic.clear()
			pic.andtag(tags,do=1)
		else:
			if md[1] == '?':
				print('默认: 生成快捷方式（速度快）\nc: 统计\ncp: 复制\ncut: 剪切')
				print('size: 格式【+.size.c.100k.>】其中c代表统计模式，默认生成快捷方式')
			elif md[1] == 'c':
				print('统计结果：%d'%len(pic.andtag(tags)))
			elif md[1] == 'cp':
				pic.clear()
				pic.andtag(tags,do=2)
			elif md[1] == 'cut':
				pic.clear()
				pic.andtag(tags)
			elif md[1] == 'size':
				step1 = pic.andtag(tags)
				if md[2] == '': 
					pic.clear()
					pic.insize(md[3],other=step1,m=md[4],do=1)
				elif md[2] == 'c':
					print('统计结果：%d'%len(pic.insize(md[3],other=step1,m=md[4])))
				elif md[2] == 'cp':
					pic.clear()
					pic.insize(md[3],other=step1,m=md[4],do=2)
				elif md[2] == 'cut':
					pic.clear()
					pic.insize(md[3],other=step1,m=md[4],do=3)
				
		pic.opc()

	elif md[0] == '-':
		if len(md) == 1:
			pic.clear()
			pic.notag(tags,do=1)
		else:
			if md[1] == 'c':
				print('统计结果：%d'%len(pic.notag(tags)))
			elif md[1] == 'cp':
				pic.clear()
				pic.notag(tags,do=2)
			elif md[1] == 'cut':
				pic.clear()
				pic.notag(tags)
			elif md[1] == 'size':
				step1 = pic.notag(tags)
				if md[2] == '': 
					pic.clear()
					pic.insize(md[3],other=step1,m=md[4],do=1)
				elif md[2] == 'c':
					print('统计结果：%d'%len(pic.insize(s,other=step1,m=md[4])))
				elif md[2] == 'cp':
					pic.clear()
					pic.insize(md[3],other=step1,m=md[4],do=2)
				elif md[2] == 'cut':
					pic.clear()
					pic.insize(md[3],other=step1,m=md[4],do=3)
		pic.opc()

	elif md[0] == '/':
		if len(md) == 1:
			pic.clear()
			pic.ortag(tags,do=1)
		else:
			if md[1] == 'c':
				print('统计结果：%d'%len(pic.ortag(tags)))
			elif md[1] == 'cp':
				pic.clear()
				pic.ortag(tags,do=2)
			elif md[1] == 'cut':
				pic.clear()
				pic.ortag(tags)
			elif md[1] == 'size':
				step1 = pic.ortag(tags)
				if md[2] == '': 
					pic.clear()
					pic.insize(md[3],other=step1,m=md[4],do=1)
				elif md[2] == 'c':
					print('统计结果：%d'%len(pic.insize(s,other=step1,m=md[4])))
				elif md[2] == 'cp':
					pic.clear()
					pic.insize(md[3],other=step1,m=md[4],do=2)
				elif md[2] == 'cut':
					pic.clear()
					pic.insize(md[3],other=step1,m=md[4],do=3)
		pic.opc()
	
	elif md[0] == '+-':
		if len(md) == 1:
			pic.clear()
			step1 = pic.andtag(tags.split('/')[0])
			pic.notag(tags.split('/')[1],other=step1,do=1)
		else:
			if md[1] == 'c':
				step1 = pic.andtag(tags.split('/')[0])
				step2 = pic.notag(tags.split('/')[1],other=step1)
				print('统计结果：%d'%len(step2))
			elif md[1] == 'cp':
				pic.clear()
				step1 = pic.andtag(tags.split('/')[0])
				pic.notag(tags.split('/')[1],other=step1,do=2)
			elif md[1] == 'cut':
				pic.clear()
				step1 = pic.andtag(tags.split('/')[0])
				pic.notag(tags.split('/')[1],other=step1,do=3)
			elif md[1] == 'size':
				step1 = pic.andtag(tags.split('/')[0])
				step2 = pic.notag(tags.split('/')[1],other=step1)
				if md[2] == '': 
					pic.clear()
					pic.insize(md[3],other=step2,m=md[4],do=1)
				elif md[2] == 'c':
					print('统计结果：%d'%len(pic.insize(s,other=step2,m=md[4])))
				elif md[2] == 'cp':
					pic.clear()
					pic.insize(md[3],other=step2,m=md[4],do=2)
				elif md[2] == 'cut':
					pic.clear()
					pic.insize(md[3],other=step2,m=md[4],do=3)
		pic.opc()
	
	elif md[0] == '-+':
		if len(md) == 1:
			pic.clear()
			step1 = pic.notag(tags.split('/')[0])
			pic.andtag(tags.split('/')[1],other=step1,do=1)
		else:
			if md[1] == 'c':
				step1 = pic.notag(tags.split('/')[0])
				step2 = pic.andtag(tags.split('/')[1],other=step1)
				print('统计结果：%d'%len(step2))
			elif md[1] == 'cp':
				pic.clear()
				step1 = pic.notag(tags.split('/')[0])
				pic.andtag(tags.split('/')[1],other=step1,do=2)
			elif md[1] == 'cut':
				pic.clear()
				step1 = pic.notag(tags.split('/')[0])
				pic.andtag(tags.split('/')[1],other=step1,do=3)
			elif md[1] == 'size':
				step1 = pic.notag(tags.split('/')[0])
				step2 = pic.andtag(tags.split('/')[1],other=step1)
				if md[2] == '': 
					pic.clear()
					pic.insize(md[3],other=step2,m=md[4],do=1)
				elif md[2] == 'c':
					print('统计结果：%d'%len(pic.insize(s,other=step2,m=md[4])))
				elif md[2] == 'cp':
					pic.clear()
					pic.insize(md[3],other=step2,m=md[4],do=2)
				elif md[2] == 'cut':
					pic.clear()
					pic.insize(md[3],other=step2,m=md[4],do=3)
		pic.opc()
	
	elif md[0] == '-/':
		if len(md) == 1:
			pic.clear()
			step1 = pic.notag(tags.split('/')[0])
			pic.ortag(tags.split('/')[1],other=step1,do=1)
		else:
			if md[1] == 'c':
				step1 = pic.notag(tags.split('/')[0])
				step2 = pic.ortag(tags.split('/')[1],other=step1)
				print('统计结果：%d'%len(step2))
			elif md[1] == 'cp':
				pic.clear()
				step1 = pic.notag(tags.split('/')[0])
				pic.ortag(tags.split('/')[1],other=step1,do=2)
			elif md[1] == 'cut':
				pic.clear()
				step1 = pic.notag(tags.split('/')[0])
				pic.ortag(tags.split('/')[1],other=step1,do=3)
			elif md[1] == 'size':
				step1 = pic.notag(tags.split('/')[0])
				step2 = pic.ortag(tags.split('/')[1],other=step1)
				if md[2] == '': 
					pic.clear()
					pic.insize(md[3],other=step2,m=md[4],do=1)
				elif md[2] == 'c':
					print('统计结果：%d'%len(pic.insize(s,other=step2,m=md[4])))
				elif md[2] == 'cp':
					pic.clear()
					pic.insize(md[3],other=step2,m=md[4],do=2)
				elif md[2] == 'cut':
					pic.clear()
					pic.insize(md[3],other=step2,m=md[4],do=3)
		pic.opc()
	
	elif md[0] == '+/':
		if len(md) == 1:
			pic.clear()
			step1 = pic.andtag(tags.split('/')[0])
			pic.ortag(tags.split('/')[1],other=step1,do=1)
		else:
			if md[1] == 'c':
				step1 = pic.andtag(tags.split('/')[0])
				step2 = pic.ortag(tags.split('/')[1],other=step1)
				print('统计结果：%d'%len(step2))
			elif md[1] == 'cp':
				pic.clear()
				step1 = pic.andtag(tags.split('/')[0])
				pic.ortag(tags.split('/')[1],other=step1,do=2)
			elif md[1] == 'cut':
				pic.clear()
				step1 = pic.andtag(tags.split('/')[0])
				pic.ortag(tags.split('/')[1],other=step1,do=3)
			elif md[1] == 'size':
				step1 = pic.andtag(tags.split('/')[0])
				step2 = pic.ortag(tags.split('/')[1],other=step1)
				if md[2] == '': 
					pic.clear()
					pic.insize(md[3],other=step2,m=md[4],do=1)
				elif md[2] == 'c':
					print('统计结果：%d'%len(pic.insize(s,other=step2,m=md[4])))
				elif md[2] == 'cp':
					pic.clear()
					pic.insize(md[3],other=step2,m=md[4],do=2)
				elif md[2] == 'cut':
					pic.clear()
					pic.insize(md[3],other=step2,m=md[4],do=3)
		pic.opc()
	
	# 统计
	elif md[0] == 'at':
		file_name_list = pic.get()[1]
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
	
	# 批量操作
	elif md[0] == 'sort':
		# 为所有文件编号
		pic.format_name()
	
	elif md[0] == 'new':
		# 为所选文件添加标签
		flist = pic.get(path=pic.cash)[1]
		for fish in flist:	#fish中包含有.lnk
			pre = ''
			shell = win32com.client.Dispatch("WScript.Shell")
			path = os.path.join(pic.cash,fish)
			shortcut = shell.CreateShortCut(path)
			target = shortcut.Targetpath
			# print(target)
			path_name = target.split('\\')
			heads = path_name[:-1]
			for head in heads:
				pre = pre+head+'\\'
			botton = path_name[-1]
			new_name = pre+tags+'.'+botton
			percent = int(((flist.index(fish)+1)/len(flist)*100)/5)
			perc = '★'*percent+'☆'*(20-percent)
			print('\r进度【'+perc+'】',end='')
			print('\n>>>：',new_name,'\n')
			os.rename(target,new_name)
		confirm = input('已添加标签。是否清空缓存文件夹？[N/any]')
		if confirm != 'N':
			pic.clear()
	
	elif md[0] == 'cut':
		# 为所选文件添加标签
		flist = pic.get(path=pic.cash)[1]
		for fish in flist:	#fish中包含有.lnk
			pre = ''
			shell = win32com.client.Dispatch("WScript.Shell")
			path = os.path.join(pic.cash,fish)
			shortcut = shell.CreateShortCut(path)
			target = shortcut.Targetpath
			# print(target)
			fts = target.split('.')
			fts[0] = fts[0].split('\\')[-1]
			nfts = []
			for ft in fts:
				if tags != ft:
					nfts.append(ft)
			newfile = '.'.join(nfts)
			
			nname = '\\'.join(target.split('\\')[:-1]) + '\\' + newfile
			# nname = nname.replace('..','.')
			# print('NNAME:',nname)
			percent = int(((flist.index(fish)+1)/len(flist)*100)/5)
			perc = '★'*percent+'☆'*(20-percent)
			print('\r进度【'+perc+'】',end='')
			print('\n>>>：',nname,'\n')
			os.rename(target,nname)
		confirm = input('已删除标签。是否清空缓存文件夹？[N/any]')
		if confirm != 'N':
			pic.clear()
	
	elif md[0] == 'deltag':
		# 删除全部文件中包含所给字段的标签
		if tags != '':
			flist = pic.get()[1]
			bag = []
			for fn in flist:
				fts = fn.split('.')
				for t in fts:
					if tags in t:
						print('Find ['+fn+'] >>>['+t+']')
						bag.append([fn,t])
						continue
				# os.system('del '+i)
			confirm = input('是否确认删除这些标签？[Y/any]')
			if confirm == 'Y':
				for it in bag:
					oname = pic.p(it[0])
					nname = oname.replace(it[1],'')
					nname = nname.replace('..','.')
					print('rename>>>',nname)
					os.rename(oname,nname)
		else:
			print('你删除个寂寞？？')

	
	print('\n'*2)
	print('当前位置：'+pic.path)
	print('缓存目录：',pic.cash)
	tags = input('请输入标签↓\n>>>').strip()
	mode = input('模式：')