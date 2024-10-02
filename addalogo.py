from PIL import Image, ExifTags
from heic2png import HEIC2PNG
import os

OUT_FOLDER = '/out'
IN_FOLDER  = '/in'
LOGO_FILE_NAME = 'logo.png'
RECOGNIZED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.heic']

files_path = os.path.dirname(os.path.realpath(__file__))

for old in os.listdir(files_path + OUT_FOLDER):
	os.remove(files_path + OUT_FOLDER + '/' + old)

watermark = Image.open(LOGO_FILE_NAME)
for image in [x for x in os.listdir(files_path + IN_FOLDER) ]:
	extension = os.path.splitext(image)[1].lower()
	name = os.path.splitext(image)[0]
	print(name, extension)
	if extension not in RECOGNIZED_EXTENSIONS:
		print(image, "Unrecognized extension")
		continue
	
	if extension == 'heic':
		heic_img = HEIC2PNG(IN_FOLDER + '/' + image, quality=90)
		heic_img.save()
		os.remove(files_path + IN_FOLDER + '/' + image)
		image = name+'.png'
	
	photo = Image.open(files_path + IN_FOLDER + '/' + image)
	#print(dir(photo))
	#break
	try:
		if photo._getexif():
			exif = dict((ExifTags.TAGS[k], v) for k, v in photo._getexif().items() if k in ExifTags.TAGS)
			#if exif['Orientation'] == 3:
			if exif.get('Orientation') == 3:
				photo = photo.rotate(180, expand=True)
			elif exif.get('Orientation') == 6:
				photo = photo.rotate(270, expand=True)
			elif exif.get('Orientation') == 8:
				photo = photo.rotate(90, expand=True)
	except:
		pass
	x, y = photo.size
	tmp_wm = watermark.resize((int(x/5), int(y/5)))
	photo.paste(tmp_wm, (int(x/2) - int(tmp_wm.size[0]/2), int(y/2) - tmp_wm.size[1]), tmp_wm)
	photo = photo.convert('RGB')
	photo.save(files_path + IN_FOLDER + '/' + image.split('.')[0] + '.jpeg', 'jpeg')
	print(image, ' --- OK')


