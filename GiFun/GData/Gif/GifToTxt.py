import os
from PIL import Image
# for i in range(0,54):
	# img = Image.open("C:/Users/111/Documents/桌面文件/GIF/" + str(i) + ".gif")
	# out = img.convert("L")
	# w = 0.4
	# h = 0.23
	# width,height = out.size
	# out = out.resize((int(width * w),int(height * h)))
	# width,height = out.size

	# asciis = "@%#&?*+=-. "
	# texts = ""
	# for row in range(height):
		# for col in range(width):
			# gray = out.getpixel((col,row))
			# texts += asciis[int (gray / 255 *10)]
		# texts += "\n"
	# with open("C:/Users/111/Documents/桌面文件/GIF/collect/" + str(i) + ".txt","w") as file:
		# file.write(texts)
	# out.close()
	
img = Image.open("D:\\#My\\python_work\\pics\\GinaLOGO.png")
out = img.convert("L")
w = 0.14
h = 0.1
width,height = out.size
out = out.resize((int(width * w),int(height * h)))
width,height = out.size

asciis = "@%#&?*+=-. "
texts = ""
for row in range(height):
	for col in range(width):
		gray = out.getpixel((col,row))
		texts += asciis[int (gray / 255 *10)]
	texts += "\n"
with open("D:\\#My\\python_work\\pics\\GinaLOGO.txt","w") as file:
	file.write(texts)
out.close()
os.system('start '+r'C:\MySoftware\Notepad++/notepad++.exe D:\\#My\\python_work\\pics\\GinaLOGO.txt')