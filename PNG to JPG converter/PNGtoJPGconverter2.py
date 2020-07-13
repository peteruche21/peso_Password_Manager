import os
from PIL import Image

file = input('enter file name in the following format (filename.ext):  ')
img = Image.open(file)
clean_name = os.path.splitext(file)[0]
img.save(f'new_{clean_name}.jpg', 'JPEG')
print(file, 'converted to jpg')
