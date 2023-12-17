from pyexiv2 import Image

root = "F:\\alpha6000\\"
img = Image(root + "2022-8-21\\DSC09427.ARW")

time_list = ['Exif.Image.DateTime', 'Exif.Photo.DateTimeOriginal', 'Exif.Photo.DateTimeDigitized']

exif = img.read_exif()

for item in time_list:
    print(exif[item])
