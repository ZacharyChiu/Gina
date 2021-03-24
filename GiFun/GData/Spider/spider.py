# 参考：https://blog.csdn.net/sl01224318/article/details/110264107

import re
import os
import requests
import time
import random
import json
from bs4 import BeautifulSoup as bs


class Huaban():
	def __init__(self):
		self.PhotoNum = 0
		self.head = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1",
					 "Cookie": "Cookie: _uab_collina=157268927148804528710717; __auc=cf088dde16e2b95dc852bfe8056; __gads=ID=a96f8b5090a1a6b1:T=1572689446:S=ALNI_Mbz7Hj7bzuE1MClpqwPgYhcWewU8w; Hm_lvt_d4a0e7c3cd16eb58a65472f40e7ee543=1610266387; uid=19641102; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAACyElEQVRYR%2BWWTUhUURTHf2dsERG0mUXhYsJASKGNTuFqpo9FmgTtaiCLzIWIzEZw2gi5KAWJGSSEJqOSZmkQhi0ix0WEX7QIKSKhIVpEg5CEu%2BbEfXOfPEcdx9DSfDDMe%2B%2Fed9%2F5nf%2F%2FnPsEVaXYISJFx%2F%2FSYHw%2BXjROMSD7FhdJtrQQSaVIRSK0JJN0dXfT2dtrwpwAGgWyxWJW8AMjwD2BB5vNVxKIeak%2FmyURjRJNJMj6%2FRi4vo4OWgcGqgTelxKYwjUzb9uCAFeAMHAVeAikBWIKPUAnkAJagItALdAAvLb3AsAoYP7PAk3AD%2BAAcKQUtU1yNqTISGMjJyaMk%2FJHJhAgkMlUAd%2BBBBAFqoF64BHQDnQB3UA%2FUAectgDm%2Fkeg0oKYJc1zBso8a84vAE9LUXxDIGtZazUQq4hbFwdtYAbEsZZCyGTcnhvLDQKm6AxIvUfRUYHx9ay7WSAZm%2Fk%2B4LzNssmquW4FYh5FXBBjOydoq8ycR5GtASmlawEdth5eAEeBNuCuzeQ3YMxaLAlEgGarhltHk8Ae%2Bztm1TH1VVJXLFmRNaXdSfvIf7Mh7loQHZ85hf56DFIO%2BhUpa0Jz5Z6aaZNwcMgkaNlcZVBOBq97E6djU%2FcRmt11JFTzyh3X9NTl%2FJq6MFwxW%2F5lv9l%2BVj%2BcT5Q%2FUSQfYC4J%2BkTCx82egaanb4J%2BciHyIFMv8%2Bv7bqHaD9qzBOkEqrdBbqCE8HFYQsEzy0CdORIbrnhXtSUg3iDdl%2BvYdByfPCvI6gzocwPrQOX47Kqi6clukHMSDtbksy8xRNpXqrLVIJ6XW2s1SDh4ackaBaqtAHFsJXUSrq3%2BpyDWTrOovgH5ieQWXJt5fL79FXFAbFZB5xBf3GuLHVMjy7qSyIfCQl2razkWUznkWKqga1mL3gEdQMrSbnec37vIUOXbze9a633kbfb4rvlE%2BQ1%2BCfYoPm%2FXEwAAAABJRU5ErkJggg%3D%3D%2CWin32.1366.768.24; sid=s%3Atn_6dPZnJbLQUPBB7v-SGW3Gnb8m6ZJS.v%2BlMRDEP2gZdj53ga25Ohje%2FHjoSaKdkcAftl9naNFc"}
		self.TimeOut = 30
		self.buff = '?iqkxaeyv&limit=200&wfl=1&max='
		self.url_image = "http://hbimg.b0.upaiyun.com/"
		self.result = []

	def get_source(self,a):

		with open('picSpace.xml','r',encoding='utf-8') as f:
			xml = bs(f.read(),'html.parser')
		beauty = eval(xml.fresh.string)['beauty']
		myfeed = eval(xml.fresh.string)['myfeed']
		photo = eval(xml.mypin.string)['web-photo']
		uiti = eval(xml.mypin.string)['uiti']  #list
		color = eval(xml.mypin.string)['color']
		try:
			return eval(a)
		except Exception as e:
			print(e)  # 关键词错误
			return 'https://huaban.com/discovery/beauty/'

	def requestUrl(self,url,lenth=1000):
		Page = requests.session().get(url, headers=self.head, timeout=self.TimeOut)
		Page.encoding = "utf-8"
		text = Page.text
		pattern = re.compile('{"pin_id":(\d*?),.*?"key":"(.*?)",.*?"like_count":(\d*?),.*?"repin_count":(\d*?),.*?}', re.S)
		items = re.findall(pattern, text)
		# print(text)
		max_pin_id = 0
		for item in items:
			max_pin_id = item[0]
			x_key = item[1]
			x_like_count = int(item[2])
			x_repin_count = int(item[3])

			url_item = self.url_image + x_key  # 图片链接地址
			print(url_item)
			if len(self.result) < lenth:
				self.result.append(url_item)
			else:
				max_pin_id = 0
				break
			self.PhotoNum += 1
		if max_pin_id != 0:
			self.requestUrl(self.urlNext + str(max_pin_id))
		else:
			print('')
	
	def bypic(self,pic_link):
		# 通过花瓣网图片链接获取图片真实地址
		# 也就是网页中的复制图片地址
		key = pic_link.split('/')[3].split('_')[0]
		url = 'http://hbimg.b0.upaiyun.com/' + key
		return url
	def byboard(self,board_id,lenth=100):
		# 通过花瓣网图片链接获取图片真实地址
		url = 'https://huaban.com/boards/' + board_id + '/'
		self.requestUrl(url,lenth)
		return self.result
	
	def log(self,urls):
		addnum = 0
		if not os.path.exists('picurls.txt'):
			with open('picurls.txt','w',encoding='utf-8') as f:
				f.write('\n'.join(urls))
			addnum = len(urls)

		else:
			with open('picurls.txt', 'r', encoding='utf-8') as f:
				has = f.readlines()
			for u in urls:
				if u.strip() not in has:
					with open('picurls.txt', 'a', encoding='utf-8') as f:
						f.write('\n'+u.strip())
					addnum += 1
		print('新增%d张图片URL链接'%addnum)

	def download(self,lenth=1000):
		if os.path.exists('picurls.txt'):
			with open('picurls.txt', 'r', encoding='utf-8') as f:
				urls = f.readlines()
			if lenth > len(urls):
				lenth = len(urls)
			for i in urls[:lenth]:
				pic = requests.get(i.strip(), timeout=10)
				percent = int(((urls.index(i) + 1) / lenth * 100) / 5)
				perc = '★' * percent + '☆' * (20 - percent)
				print('\r进度【' + perc + '】', end='')
				with open('spider/pics/' + str(urls.index(i)+1)+'.jpg','wb') as f:
					f.write(pic.content)
		else:
			print('没有资源文件')

	def run(self,ask,lenth=1000):
		self.result = []
		self.url = self.get_source(ask)
		# print(self.url)
		if type(self.url) == list:
			for u in self.url:
				self.urlNext = u + self.buff
				self.requestUrl(u,lenth=lenth)
		else:
			self.urlNext = self.url + self.buff
			self.requestUrl(self.url,lenth=lenth)

		return self.result

class Moji():
	def __init__(self):
		self.url = "https://tianqi.moji.com/forecast15/china/jiangsu/yixing"
		self.todayurl = "https://tianqi.moji.com/today/china/jiangsu/yixing"
		self.wea15 = self.get15wea()
		self.now = self.today()

	def get15wea(self):
		head = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
		TimeOut = 30
		ans = []
		Page = requests.session().get(self.url, headers=head, timeout=TimeOut)
		Page.encoding = "utf-8"
		self.html = bs(Page.text,'html.parser')
		weather_block = self.html.find_all('div',class_='wea_list clearfix')[0]
		weather_bar = weather_block.ul.find_all('li')
		for i in weather_bar:
			day = i.find_all('span',class_='week')  #[星期, 日期]
			week = day[0].string
			date = day[1].string
			weather = i.find_all('span',class_='wea')  # [0] 转 [1]
			wen = i.find_all('div',class_='tree clearfix')[0].p
			wen_1 = wen.b.string  # 最高温
			wen_0 = wen.strong.string  # 最低温
			if len(set(weather)) == len(weather):
				wea = weather[0].string + '转' + weather[1].string
			else:
				wea = weather[0].string

			info = [date,week,wea,wen_1,wen_0]

			ans.append(info)
			# print(info)
			# print('='*20)
		return ans
	def today(self):
		head = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
		TimeOut = 30
		ans = []
		Page = requests.session().get(self.todayurl, headers=head, timeout=TimeOut)
		Page.encoding = "utf-8"
		self.html = bs(Page.text,'html.parser')
		weather_today = self.html.find_all('div',class_='info clearfix')[0]
		# print(weather_today)
		wea = weather_today.b.string
		wen = weather_today.em.string
		return [wea,wen]

class City():
	def __init__(self):
		self.url = 'http://xzqh.mca.gov.cn/map'
	def get_citys(self):
		head = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
		TimeOut = 30
		ans = []
		Page = requests.get(self.url, headers=head, timeout=TimeOut)
		Page.encoding = "GBK"  # 注意网页源代码header中的编码方式。这里用utf-8显示不出中文
		self.html = bs(Page.text,'html.parser')
		aa = self.html.find_all('table',class_='select_table')[1]
		bb = aa.find_all('input',id="pyArr")[0].attrs
		citys = eval(bb['value'])  # list
		cc = []
		for i in citys:
			cc.append(i['cName'])
		return cc
	def province(self,p):
		citys = self.get_citys()
		for i in citys:
			if p in i['cName']:
				p_0 = citys.index(i)
				# print('start:%d'%p_0)
				for j in citys[p_0+1:]:
					if '省' in j['cName']:
						p_1 = citys.index(j)
						# print('end:%d'%p_1)
						break
		return citys[p_0:p_1]

def web_order():
	url = 'https://huaban.com/boards/66843722/'
	head = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
	TimeOut = 30
	ans = []
	Page = requests.session().get(url, headers=head, timeout=TimeOut)
	Page.encoding = "utf-8"
	html = bs(Page.text,'html.parser')
	title = html.head.title.string
	order = title.split('_')[0].split('(')[0]
	return order


if __name__ == '__main__':
	hua = Huaban()
	result = hua.bypic('https://hbimg.huabanimg.com/7abf394f9195bede141baf33c2f7504155fb2e0310086f-FvnI4W_fw658/format/webp')
	# os.system('C:\\quickstart\\gg.lnk '+result)
	# w = Moji()
	# print(w.now)
