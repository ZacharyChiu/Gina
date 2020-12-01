'''手势控制程序'''
from aip import AipBodyAnalysis
import cv2
import time
from pymouse import *
from pykeyboard import PyKeyboard
""" 你的 APPID AK SK """
APP_ID = '19460689'
API_KEY = '3RPwP6fPGBAFxaDu4uTqrjSL'
SECRET_KEY = '42q3U4GUzxnqGBsBG8kkV3Lt8axuqLDa'

client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)
""" 读取图片 """
sign_dic = {'One':'1','Two':'2','Three':'3','Four':'4','Five':'5','Six':'6','Seven':'7','Eight':'8','Nine':'9','Ok':'OK','Fist':'拳','Prayer':'合十',
	'Congratulation':'抱拳','Honour':'承让','Heart_single':'比心','Thumb_up':'赞','Thumb_down':'踩','ILY':'爱','Palm_up':'托','Heart_1':'','Heart_2':'','Heart_3':'','Rock':'Rock','Insult':'Fuck','xxx':'None','Face':'Face'}
# 创建虚拟鼠标键盘
ms = PyMouse()
kb = PyKeyboard()

while True:
	#拍照
	cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
	ret,frame = cap.read()
	# cv2.imshow('capture',frame)

	cv2.imwrite('photo.jpg',frame)
	cap.release()
	cv2.destroyAllWindows()

	def get_file_content(filePath):
		with open(filePath, 'rb') as fp:
			return fp.read()

	image = get_file_content('photo.jpg')

	""" 调用手势识别 """
	answer = client.gesture(image)
	try:
		result = answer['result'][0]['classname']
	except:
		result = 'xxx'
	hand = sign_dic[result]
	print('\r'+hand+'           ',end='')
	if hand == '5':
		kb.press_keys([kb.menu_key,'q'])
		kb.release_key('q')
		kb.release_key(kb.space_key)
		
	elif hand == '2':
		kb.press_keys([kb.menu_key,kb.right_key])
		kb.release_key(kb.right_key)
		kb.release_key(kb.menu_key)
	elif hand == 'OK':
		kb.press_keys([kb.menu_key,kb.left_key])
		kb.release_key(kb.left_key)
		kb.release_key(kb.menu_key)
	elif hand == '赞':
		kb.press_keys([kb.menu_key,kb.up_key])
		kb.release_key(kb.up_key)
		kb.release_key(kb.menu_key)
	elif hand == '踩':
		kb.press_keys([kb.menu_key,kb.down_key])
		kb.release_key(kb.down_key)
		kb.release_key(kb.menu_key)
	elif hand == '3':
		kb.press_keys([kb.windows_l_key,kb.down_key])
		kb.release_key(kb.down_key)
		kb.release_key(kb.windows_l_key)
	elif hand == '抱拳':
		kb.press_keys([kb.windows_l_key,kb.up_key])
		kb.release_key(kb.up_key)
		kb.release_key(kb.windows_l_key)
	elif hand == '7':
		kb.press_key(kb.enter_key)
		kb.release_key(kb.enter_key)
	elif hand == 'Fuck':
		kb.press_key(kb.escape_key)
		kb.release_key(kb.escape_key)
	elif hand == '9':
		kb.press_key(kb.down_key)
		kb.release_key(kb.down_key)
	elif hand == '8':
		kb.press_key(kb.up_key)
		kb.release_key(kb.up_key)
	elif hand == '爱':
		kb.press_key(kb.right_key)
		kb.release_key(kb.right_key)
	elif hand == 'Rock':
		kb.press_key(kb.left_key)
		kb.release_key(kb.left_key)
	# elif hand == '比心':	
		# kb.press_keys([kb.menu_key,'l'])
		# kb.release_key('l')
		# kb.release_key(kb.menu_key)
	elif hand == '6':
		kb.press_keys([kb.menu_key,kb.tab_key])
		# kb.release_key(kb.tab_key)
		# kb.release_key(kb.menu_key)
	elif hand == '4':
		kb.press_keys([kb.control_key,kb.menu_key,'t'])
	elif hand == '比心':
		kb.press_keys([kb.control_key,kb.menu_key,'g'])