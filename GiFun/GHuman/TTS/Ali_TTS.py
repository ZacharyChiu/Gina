# -*- coding: utf-8 -*-
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import ali_speech
from ali_speech.callbacks import SpeechSynthesizerCallback
from ali_speech.constant import TTSFormat
from ali_speech.constant import TTSSampleRate
import threading
import os
import pygame
import time
from mutagen.mp3 import MP3
import pyperclip
import re



def play_music(path, f=22050):
	audio = MP3(path)
	length = float(audio.info.length)
	pygame.mixer.init(frequency=f)
	pygame.mixer.music.load(path)
	pygame.mixer.music.play()
	time.sleep(length)
	pygame.mixer.music.stop()


def get_aliyun_secret(AKID, AS):
	client = AcsClient(AKID, AS, 'cn-shanghai')
	request = CommonRequest()
	request.set_method('POST')
	request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
	request.set_version('2019-02-28')
	request.set_action_name('CreateToken')
	r = client.do_action_with_exception(request)
	r = json.loads(r.decode())
	return r['Token'].get('Id')


class MyCallback(SpeechSynthesizerCallback):
	# 参数name用于指定保存音频的文件
	def __init__(self, name, mode):
		self._name = name
		self.mode = mode
		# ab+  追加模式
		# wb+  写模式
		self._fout = open(name, mode)

	def on_binary_data_received(self, raw):
		# print('MyCallback.on_binary_data_received: %s' % len(raw))
		self._fout.write(raw)

	def on_completed(self, message):
		# print('MyCallback.OnRecognitionCompleted: %s' % message)
		self._fout.close()

	def on_task_failed(self, message):
		# print('MyCallback.OnRecognitionTaskFailed-task_id:%s, status_text:%s' % (
		# message['header']['task_id'], message['header']['status_text']))
		self._fout.close()
	# def on_channel_closed(self):
	# print('MyCallback.OnRecognitionChannelClosed')


def process(client, appkey, token, text, audio_name, she='Aixia', sound=[100,0,0], mode='wb'):
	callback = MyCallback(audio_name,mode)
	synthesizer = client.create_synthesizer(callback)
	synthesizer.set_appkey(appkey)
	synthesizer.set_token(token)
	synthesizer.set_voice(she)
	synthesizer.set_text(text)
	synthesizer.set_format(TTSFormat.MP3)
	synthesizer.set_sample_rate(TTSSampleRate.SAMPLE_RATE_16K)
	synthesizer.set_volume(sound[0])
	synthesizer.set_speech_rate(sound[1])
	synthesizer.set_pitch_rate(sound[2])
	try:
		ret = synthesizer.start()
		if ret < 0:
			return ret
		synthesizer.wait_completed()
	except Exception as e:
		print(e)
	finally:
		synthesizer.close()


def process_multithread(client, appkey, token, number):
	thread_list = []
	for i in range(0, number):
		text = "这是线程" + str(i) + "的合成。"
		audio_name = "sy_audio_" + str(i) + ".mp3"
		thread = threading.Thread(target=process, args=(client, appkey, token, text, audio_name))
		thread_list.append(thread)
		thread.start()
	for thread in thread_list:
		thread.join()

client = ali_speech.NlsClient()
appkey = 'hPUZhaSWHkUp4NwM'
AKID = 'LTAI4FyftcdsKMv6JcKcTvqv'
AS = 'edjIOVArss0vPVSHKlJrjHh0XTwyHf'
token = get_aliyun_secret(AKID,AS)
sound = [100,-100,0]

def spstr(text, audio_name, l=280):
	pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！|？|…|（|）|”|\n'
	biao = False
	for i in pattern:
		if i in text:
			if text[-1] not in pattern:
				text += '。'
			biao = True
	print("有标点吗：",biao)
	if biao:
		## 对于过长文本进行分段写入 ##
		temp_t = text[:l]
		end_half = re.split(pattern, temp_t)[-1]
		print('结尾：',end_half)
		if end_half == '':
			print('>>>切得正好！')
		else:
			print('>>>修剪一下。')
			temp_t = temp_t[:-1*len(end_half)]
		n_text = text[len(temp_t):]
		print('断段：',temp_t)
		print('剩余字符长度：【',len(n_text),'】')
		# print('【此处将$'+temp_t+'$写入MP3】')
		process(client, appkey, token, temp_t, audio_name,
				she='Aixia',
				sound=sound,
				mode='ab'
				)
		if len(n_text)>0:
			spstr(n_text,audio_name)
	else:
		process(client, appkey, token, text, audio_name,
				she='Aixia',
				sound=sound,
				mode='wb'
				)


yin = [
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


def readit(text, title):
	try:
		os.remove(title)
		print('已删除原有音频……')
	except:
		print('直接写入……')
	spstr(text,title)  # 生产语音合成文件


if __name__ == "__main__":
	'''===============配置================'''
	sound = [100,-100,0]  # [音量，语速，语调]
	she = yin[30]  # 声优
	she = 'Aixia'
	mode = 'ab'  # 追加模式写入文件
	play = 0  # 播放模式：1-直接放；0-外部播放
	'''==================================='''
	mode = input('Mode:')
	if mode == "1":
		text = input('Text: ')
		# title = 'test'  # 文件标题
		title = input('文件名：')
		while text != 'q':
			client = ali_speech.NlsClient()
			# 设置输出日志信息的级别：DEBUG、INFO、WARNING、ERROR
			# client.set_log_level('INFO')
			appkey = 'hPUZhaSWHkUp4NwM'
			AKID = 'LTAI4FyftcdsKMv6JcKcTvqv'
			AS = 'edjIOVArss0vPVSHKlJrjHh0XTwyHf'
			token = get_aliyun_secret(AKID,AS)
			audio_name = 'D:\\#My\\GiData\\Creation\\Designs\\Audios\\'+title+'.mp3'

			try:
				os.remove(audio_name)
				print('已删除原有音频……')
			except:
				print('直接写入……')
			spstr(text,title)  # 生产语音合成文件

			if play == 1:
				play_music(audio_name)
			elif play == 0:
				os.system(audio_name)
			text = input('Text: ')
			title = input('文件名：')
	else:
		text = pyperclip.paste()
		title = input('文件名：')

		client = ali_speech.NlsClient()
		# 设置输出日志信息的级别：DEBUG、INFO、WARNING、ERROR
		# client.set_log_level('INFO')
		appkey = 'hPUZhaSWHkUp4NwM'
		AKID = 'LTAI4FyftcdsKMv6JcKcTvqv'
		AS = 'edjIOVArss0vPVSHKlJrjHh0XTwyHf'
		token = get_aliyun_secret(AKID,AS)
		audio_name = title+'.mp3'

		try:
			os.remove(audio_name)
			print('已删除原有音频……')
		except:
			print('直接写入……')
		spstr(text,title)  # 生产语音合成文件

		# process(client, appkey, token, text, audio_name,
				# she=she,
				# sound=sound,
				# )
		os.rename('test','test.mp3')
	play_music(audio_name,16000)
	# if play == 1:
	# elif play == 0:
		# os.system(audio_name)

	# print(os.getcwd()+'\\sy_audio.wav')
	# play_music(os.getcwd()+'\\sy_audio.wav')
	# 多线程示例
	# process_multithread(client, appkey, token, 2)
