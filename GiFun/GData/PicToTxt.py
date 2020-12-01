def ptt():
	from PIL import Image
	img = Image.open("trans.jpg")
	out = img.convert("L")
	w = 0.5
	h = 0.25
	width,height = out.size
	out = out.resize((int(width * w),int(height * h)))
	width,height = out.size

	asciis = "@%#&?*+=-. "
	#asciis = "饢操四尔三二一· "
	texts = ""
	for row in range(height):
		for col in range(width):
			gray = out.getpixel((col,row))
			texts += asciis[int (gray / 255 *10)]
		texts += "\n"
	with open("asciis.txt","w") as file:
		file.write(texts)
	out.close()
