# 智能时钟程序
# 创建者：Zachary
'''
目标：
1.显示时间；
2.获取天气；
3.实现计时功能；
4.实现闹钟。
'''
import datetime
import time
import pygame
import requests
from urllib import request
from bs4 import BeautifulSoup


def show_time():
	cur_time = datetime.datetime.now()	# 数据类型为：datetime
	print('\r#',str(cur_time).split('.')[0],end='')
	
def show_weather(city):
	url = 'https://tianqi.moji.com/weather/china/jiangsu/' + city
	htmlData = request.urlopen(url).read().decode('utf-8')
	soup = BeautifulSoup(htmlData, 'lxml')
	# print(soup.prettify())
	weather = soup.find('div',attrs={'class':"wea_weather clearfix"})
	T = weather.find('em').get_text()
	W = weather.find('b').get_text()
	print('\t','宜兴',T+'℃',W,end='')


while True:
	show_time()
	show_weather('yixing')
	