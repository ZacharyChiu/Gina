# 文件备份程序

import os
from hashlib import md5
from shutil import copyfile

def ha(file_path):
    md5_1 = md5()  #创建一个md5算法对象
    with open(file_path,'rb') as f:  #打开一个文件，必须是'rb'模式打开
        md5_1.update(f.read())
    ret = md5_1.hexdigest()  #获取这个文件的MD5值
    return ret
def get_k(d,value):
    for k,v in d.items():
        if v == value:
            return k

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

def clear_dir(path):
    name_list = os.listdir(path)
    for c in name_list:
        dpath = path+'\\'+c
        os.remove(dpath)
        index = name_list.index(c)
        percent = int(((index+1)/len(name_list)*100)/5)
        perc = '★'*percent+'☆'*(20-percent)
        print('\r正在删除>>>%d/%d【%s】'%(index+1,len(name_list),perc),end='')
        
        
# o_path = 'D:\\Zac\\python\\backup\\sth'  # 源文件路径
o_path = 'D:\\#My\\GiData\\Source\\Arts\\Images\\Pics'
n_path = 'E:\\Gidata\\Source\\Arts\\Images\\pic'  # 备份文件路径

rename_all = False
no_change = False


o_files = clean(os.listdir(o_path))
n_files = clean(os.listdir(n_path))
o_has = {}
n_has = {}
full_len = len(o_files)


mode = input('Mode:')
if mode == 'backup':
    
    # 导入源文件列表
    if o_files:
        for f in o_files:
            hh = ha(o_path+'\\'+f)
            o_has[f] = hh
            index = o_files.index(f)
            percent = int(((index+1)/full_len*100)/5)
            perc = '★'*percent+'☆'*(20-percent)
            print('\r计算源文件哈希>>>%d/%d【%s】'%(index+1,full_len,perc),end='')

    if len(set(o_has.values())) != len(o_has.values()):
        print('\n警告：源文件夹好像有重复文件噢！')

    # 导入备份文件列表
    for f in n_files:
        hh = ha(n_path+'\\'+f)
        n_has[f] = hh
        index = n_files.index(f)
        percent = int(((index+1)/len(n_files)*100)/5)
        perc = '★'*percent+'☆'*(20-percent)
        print('\r计算备份文件哈希>>>%d/%d【%s】'%(index+1,len(n_files),perc),end='')

    # print('源：',o_has)
    # print('备：',n_has)


    print(full_len)
    print('='*30)

    for k,v in o_has.items():
        index = list(o_has.values()).index(v)
        percent = int(((index+1)/full_len*100)/5)
        perc = '★'*percent+'☆'*(20-percent)
        if v not in n_has.values():
            # print(k)
            copyfile(o_path+'\\'+k,n_path+'\\'+k)
            n_has[k] = v
        else:
            o_name = get_k(o_has,v)
            n_name = get_k(n_has,v)
            if len(set(o_has.values())) == len(o_has.values()):
                if o_name != n_name:
                    print('发现【%s】的名字更新为了【%s】'%(n_name,o_name))
                    if not rename_all:
                        yon = input('是否更新名字？[y/Y/any]')
                        if yon == 'y':
                            os.rename(n_path+'\\'+n_name,n_path+'\\'+o_name)
                            print('Done!')
                        elif yon == 'Y':
                            rename_all = True
                    if rename_all:
                        os.rename(n_path+'\\'+n_name,n_path+'\\'+o_name)
                        print('Rename all!')
                else:
                    no_change = True
        print('\r备份中>>>%d/%d【%s】'%(index+1,full_len,perc),end='')
    if no_change:
        print('\n源文件夹好像没有变动呢！')

elif mode == 'call':
     clear_dir(n_path)


# print('76291f4bc15674327089fbe0ec3ccaa7' in o_has.values())
