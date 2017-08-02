#!/usr/bin/python

from PIL import Image

qr = Image.new('RGB',(200,200))
black = Image.open('black.png')
white = Image.open('white.png')

for row in range(25):
	for column in range(25):
		if (((row * column) % 2) + ((row * column) % 3) == 0):
			qr.paste(black, (row * 8, column * 8))
		else:
			qr.paste(white, (row * 8, column * 8))

qr.save('mask5.png')