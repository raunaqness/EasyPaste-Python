import qrcode
from PIL.ImageQt import ImageQt

def get_qrimage(text):
	img = qrcode.make(text)
	qimg = ImageQt(img)
	return(qimg)