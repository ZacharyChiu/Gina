# -*- coding: utf-8 -*-
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import ali_speech
from ali_speech.callbacks import SpeechSynthesizerCallback
from ali_speech.constant import TTSFormat
from ali_speech.constant import TTSSampleRate
import os
import pygame
import time
import datetime
from mutagen.mp3 import MP3
import pyperclip
import re


class MyCallback(SpeechSynthesizerCallback):
	# 参数name用于指定保存音频的文件
	def __init__(self, name, mode):
		self._name = name
		self.mode = mode
		# ab+  追加模式
		# wb+  写模式
		self._fout = open(name, mode)

	def on_binary_data_received(self, raw):
		self._fout.write(raw)

	def on_completed(self, message):
		self._fout.close()

	def on_task_failed(self, message):
		self._fout.close()


class Speech():
	def __init__(self):
		self.client = ali_speech.NlsClient()
		self.appkey = 'hPUZhaSWHkUp4NwM'
		self.AKID = 'LTAI4FyftcdsKMv6JcKcTvqv'
		self.AS = 'edjIOVArss0vPVSHKlJrjHh0XTwyHf'
		self.token = self.get_aliyun_secret()
		self.sound = [100,-100,0]
		self.yin = [
			##通用场景##
			'Xiaoyun',  #0
			'Ruoxi','Siqi','Sijia','Aiqi','Aijia',  #1-5
			'Ninger','Ruilin',  #6,7
			##客服场景##
			'Siyue','Aiya','Aimei',  # 8-10
			'Aiyu','Aiyue','Aijing','Xiaomei','Aina',  #11-15
			'Yina','Sijing',  #16,17
			##儿童##
			'Sitong','Xiaobei','Aitong','Aiwei','Aibao',  #18-22
			##英语##
			'Abby','Emily','Luna','Wendy','Olivia',  #23-27
			'Lydia',  # 英中双语
			##方言##
			# 粤；川；台；东北
			'Shanshan','Xiaoyue','Qingqing','Cuijie',	#29-32
			]
		self.she = 'Aixia'  # 声优
		self.mode = 'ab'  # 追加模式写入文件
		self.sounds_dir = r'D:\#My\GiData\Creation\Projects\Python\Gina\GiFun\GHuman\sounds'

	def play_music(self, path, f=16000, delay=0):
		pygame.mixer.init(frequency=f)
		pygame.mixer.music.load(path)
		pygame.mixer.music.play()
		audio = MP3(path)
		if delay != 'x':
			# 等待播放完后再执行后面脚本
			if audio.info.length-delay >= 0:
				d = audio.info.length-delay
			else:
				d = audio.info.length
		else:
			# delay为x时，不等待
			d = 0
		time.sleep(d)
		# print('Playing:[%s]'%(str(int(d)+1)))
		
	
	def say(self,oo,t=0,dir='xxx'):
		# oo为音频文件名（不带后缀），oo可以为列表
		if dir == 'xxx':
			dir = self.sounds_dir
		elif dir == '':
			dir = os.getcwd()
		
		if type(oo) == type([]):
			mus = []
			for m in oo:
				sound = dir + '\\' + m + '.mp3'
				mu = AudioSegment.from_mp3(sound)
				mus.append(mu)
			music = mus[0]
			for i in mus[1:]:
				music += i
			music.export("temp.mp3", format="mp3")
		else:
			sound = dir + '\\' + oo + '.mp3'
			self.play_music(sound,delay=t)
	
	def timelog(self):
		# 生成当前时间14位代码，不可能重复。
		cur_time = datetime.datetime.now()  # 数据类型为：datetime
		now = str(cur_time).split('.')[0]
		date = ''.join(now.split(' ')[0].split('-'))
		time = ''.join(now.split(' ')[1].split(':'))
		t = date + time
		return t  # 字符串，例：20210511041522 -> 21年5月11日4点15分22秒
	
	def get_aliyun_secret(self):
		client = AcsClient(self.AKID, self.AS, 'cn-shanghai')
		request = CommonRequest()
		request.set_method('POST')
		request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
		request.set_version('2019-02-28')
		request.set_action_name('CreateToken')
		r = client.do_action_with_exception(request)
		r = json.loads(r.decode())
		return r['Token'].get('Id')

	def process(self,text, audio_name):
		callback = MyCallback(audio_name,self.mode)
		synthesizer = self.client.create_synthesizer(callback)
		synthesizer.set_appkey(self.appkey)
		synthesizer.set_token(self.token)
		synthesizer.set_voice(self.she)
		synthesizer.set_text(text)
		synthesizer.set_format(TTSFormat.MP3)
		synthesizer.set_sample_rate(TTSSampleRate.SAMPLE_RATE_16K)
		synthesizer.set_volume(self.sound[0])
		synthesizer.set_speech_rate(self.sound[1])
		synthesizer.set_pitch_rate(self.sound[2])
		try:
			ret = synthesizer.start()
			if ret < 0:
				return ret
			synthesizer.wait_completed()
		except Exception as e:
			print(e)
		finally:
			synthesizer.close()

	def spstr(self,text, audio_name, l=280):
		pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！|？|…|（|）|”|\n'
		biao = False
		for i in pattern:
			if i in text:
				if text[-1] not in pattern:
					text += '。'
				biao = True
		# print("有标点吗：",biao)
		if biao:
			## 对于过长文本进行分段写入 ##
			temp_t = text[:l]
			end_half = re.split(pattern, temp_t)[-1]
			# print('结尾：',end_half)
			if end_half == '':
				# print('>>>切得正好！')
				print('')
			else:
				# print('>>>修剪一下。')
				temp_t = temp_t[:-1*len(end_half)]
			n_text = text[len(temp_t):]
			# print('断段：',temp_t)
			# print('剩余字符长度：【',len(n_text),'】')
			# print('【此处将$'+temp_t+'$写入MP3】')
			self.process(temp_t, audio_name)
			if len(n_text)>0:
				self.spstr(n_text,audio_name)
		else:
			self.process(text, audio_name)

	def main(self,words,name):
		# 语音合成
		audio_name = name+".mp3"

		try:
			os.remove(audio_name)
			# print('已删除原有音频……')
		except:
			# print('直接写入……')
			pass
		self.spstr(words,name)  # 生产语音合成文件
	
	def speak(self,text,name='',dir='xxx',addit=0,t=0):
		# 语音合成并生成音频文件
		# t='x'时，声音播放不暂停动作
		if dir == 'xxx':
			dir = self.sounds_dir
		
		if addit == 0:
			if name == '':
				name = self.timelog()
			self.main(text,name + '.mp3')
			# with open('tts_logs\\log_dic.txt','a',encoding='utf-8') as f:
				# f.write(name+'\t'+text+'\n')
			self.say(name,dir=dir,t=t)
			return name 
		else:
			self.main(text,dir + '\\' + name + '.mp3')
			self.say(name,t=t)
			return dir + '\\' + name


def test():
	content = '你是啥玩意儿？'
	speech = Speech()

	# 检测音库是否已有
	with open('log_dic.txt','r',encoding='utf-8') as f:
		log_list = f.readlines()
		logname = []
		logcontent = []
		for l in log_list:
			if l[0] != '#':
				aaa = l.split('\t')[0]
				bbb = '\t'.join(l.split('\t')[1:]).strip()
				if bbb not in logcontent:
					logcontent.append(bbb)
					logname.append(aaa)
	if content in logcontent:
		speech.say(logname[logcontent.index(content)],dir='')
	else:
		log_name = speech.speak(content,name=speech.timelog(),dir='').split('\\')[-1]
		with open('log_dic.txt','a',encoding='utf-8') as f:
			f.write(log_name+'\t'+content+'\n')
		print('-'*50)
	print(content)

if __name__ == "__main__":
	# print(os.getcwd())
	test()
	test()
	test()
