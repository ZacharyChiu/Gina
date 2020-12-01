from aip import AipFace
import base64

APP_ID = '15897329'
API_KEY = 'xtNaN8HBQ7rSr9L0R4R8OmVj'
SECRET_KEY = 'qtk2DUfSFPGFbqw007mSuLdgEMECtQOn'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)

#模式选择
mode = input('选择模式(默认本地模式，w为网页模式，p为现场拍照)\n')
if mode == 'p':
	import cv2
	#拍照
	cap = cv2.VideoCapture(0)
	while(1):
		ret,frame = cap.read()
		cv2.imshow('capture',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.imwrite('D:\\#My\\python_work\\Api_Face\\photo.jpg',frame)
			break
	cap.release()
	cv2.destroyAllWindows()
	filePath = 'D:\\#My\\python_work\\Api_Face\\photo.jpg'
	#base64编码处理文件
	with open(filePath,"rb") as f:
		base64_data = base64.b64encode(f.read())

	image = str(base64_data,'utf-8')
	imageType = "BASE64"

elif mode == 'w':
	imageType = "URL"
	'''图片网址在这里改！'''
	image = input('网址(必须以图片文件格式结尾)：')
	#image = 'https://huaban.com/pins/2367378867/'
else:
	'''本地图片路径在这里改！'''
	#filePath = 'C:\\Users\\111\\Documents\\桌面文件\\3.jpg'
	Path = input('图片路径：')
	filePath = []
	for index in range(len(Path)):
		if Path[index] == '\\':
			filePath.append('/')
			continue
		else:
			filePath.append(Path[index])
	filePath = ''.join(filePath)
	#base64编码处理文件
	with open(filePath,"rb") as f:
		base64_data = base64.b64encode(f.read())

	image = str(base64_data,'utf-8')
	imageType = "BASE64"



""" 调用人脸检测 """
client.detect(image, imageType);

""" 如果有可选参数 """
options = {}
options["face_field"] = "age,beauty,gender,race,quality,facetype"
options["max_face_num"] = 1
options["face_type"] = "LIVE"

""" 带参数调用人脸检测 """
result = client.detect(image, imageType, options)

#结果赋值
gender = result['result']['face_list'][0]['gender']['type']
age = result['result']['face_list'][0]['age']
beauty = result['result']['face_list'][0]['beauty']

print('性别：',gender,'年龄：',age,'颜值',beauty)

input('END')