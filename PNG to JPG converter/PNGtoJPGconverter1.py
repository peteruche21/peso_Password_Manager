import os, pdb
from PIL import Image


converted = 'new'

if not os.path.exists(fr'{converted}'):
    os.mkdir(f'{converted}')

for root, dirs, files in os.walk(fr'.'):
    for file in files:
        if file.endswith('.png'):
            conv = Image.open(f'{file}')
            clean_name = os.path.splitext(file)[0]
            conv.save(f'{converted}/{clean_name}.jpg', 'JPEG')
            print(file, 'converted to jpg')
