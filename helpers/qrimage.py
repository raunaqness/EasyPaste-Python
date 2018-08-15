import qrcode

def create_qrimage(text):
	img = qrcode.make(text)
	return(img)