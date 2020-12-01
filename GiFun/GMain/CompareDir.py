import os
from hashlib import md5


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

def get_md5(file_path):
	md5_1 = md5()  #创建一个md5算法对象
	with open(file_path,'rb') as f:  #打开一个文件，必须是'rb'模式打开
		md5_1.update(f.read())
	ret = md5_1.hexdigest()  #获取这个文件的MD5值
	return ret
	


o_path = "D:\\#My\\Picture\\Hl'Tu'\\Lu-Ys,"
# o_path = 'D:\\#My\\GiData\\Source\\Arts\\Images\\untag'

pic_path = 'D:\\#My\\GiData\\Source\\Arts\\Images\\Pics'

o_list = clean(os.listdir(o_path))
pic_list = clean(os.listdir(pic_path))
p_md_list = []  # 所有图片hash
o_md_list = []
p_index = []
with open('PIC_Hash.csv','r',encoding='utf-8') as f:
	for l in f.readlines():
		p_md_list.append(l.split(',')[-1].strip())
		p_index.append(l.split(',')[0].strip())
# for m in p_md_list:
	# print('#%s#'%m)
	
# for p in pic_list:
	# md = get_md5(pic_path+'\\'+p)
	# p_md_list.append(md)
	# print('\rComputing: [%d/%d]   '%(pic_list.index(p)+1,len(pic_list)),end='')
# print('\r'*2)
for p in o_list:
	md = get_md5(o_path+'\\'+p)
	o_md_list.append(md)
	print('\rComputing: [%d/%d]   '%(o_list.index(p)+1,len(o_list)),end='')

save = input('Save?[Y/any]')
csv_text = 'Index,Hash\n'
if save == 'Y':
	for i in range(len(p_md_list)):
		line = pic_list[i].split('.')[-2] +','+p_md_list[i]+'\n'
		csv_text = csv_text + line
	with open('PIC_Hash.csv','w',encoding='utf-8') as f:
		f.write(csv_text)
	print('Saved!')


rr = []
de = input('Remove them?[Y/any]')
for i in range(len(o_md_list)):
	for j in range(len(p_md_list)):
		if o_md_list[i] == p_md_list[j]:
			rr.append(o_list[i])
			print('%d | 【%s】与【%s号】重复'%(i+1,o_list[i],p_index[j]))
			if de == 'Y':
				os.remove(o_path+'\\'+o_list[i])
			
if de == 'Y':
	print('已删除所有重复项！！！！')