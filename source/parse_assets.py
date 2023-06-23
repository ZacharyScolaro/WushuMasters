import math
import png

palette = []

y = 0;

def parse_palette(png_name):
	global palette;
	y = 0;
	f = open('../assets/' + png_name, 'rb')
	r = png.Reader(f)
	width, height, rows, info = r.read()
	pixel_width = width // 8
	pixel_height = height // 16
	planes = info['planes']
	pixel_y = 0
	palette = []
	for row in rows:
		if y % pixel_height == pixel_height // 2:
			for x in range(0, 8, 1):
				offset = ((x * pixel_width) + (pixel_width // 2)) * planes
				color = (row[offset], row[offset+1], row[offset+2])
				palette.append(color)
			pixel_y = pixel_y + 1
		y+=1
	f.close()

def rgb_to_colu(rgb):
	closest = 0
	min_dist = 256*256*256
	for i in range(0,128):
		dist = math.sqrt((rgb[0] - palette[i][0])**2 +(rgb[1] - palette[i][1])**2 + (rgb[2] - palette[i][2])**2)
		if dist < min_dist:
			min_dist = dist
			closest = i
	return closest * 2


def parse_png(png_name, pixel_width, pixel_height, item_x, item_y, item_width, item_height, alpha_color):
	global y
	y = 0

	graphic_bytes = []
	color_bytes = []

	f = open('../assets/' + png_name, 'rb')
	r = png.Reader(f)
	width, height, rows, info = r.read()
	print(info)
	planes = info['planes']
	print(width, height, pixel_width, planes)
	pixel_y = 0
	for row in rows:
		if y % pixel_height == 0:
			if pixel_y >= item_y:
				colu = 0
				b = 0
				mask = 0x80
				for x in range(item_x*pixel_width*planes, (item_x + item_width)*pixel_width*planes, pixel_width*planes):
					color = (row[x], row[x+1], row[x+2])
					if color  != alpha_color:
						b |= mask
						colu = rgb_to_colu(color)
					mask = mask >> 1
					if mask == 0:
						graphic_bytes.append('0x{:02x}'.format(b))
						b = 0
						mask = 0x80
				if mask != 0x80:
					graphic_bytes.append('0x{:02x}'.format(b))
				color_bytes.append('0x{:02x}'.format(colu))
			pixel_y = pixel_y + 1
			if pixel_y >= item_y + item_height:
				break
		y+=1
	f.close()
	return graphic_bytes, color_bytes

def parse_sprite_strip(f_header, f_source, png_name, item_name, item_width, item_height, item_count, pixel_width, pixel_height, item_x, item_y, alpha_color):
	color_bytes = None
	item_size = math.ceil(item_width/8) * item_height # figure out how many bytes to hold it all
	first_dimension = '[' + str(item_count) + ']' if item_count > 1 else ''
	f_header.write('\nextern const uint8_t ' + item_name + 'Graphics' + first_dimension + '[' + str(item_size) + '];\n')
	f_source.write('\nconst uint8_t ' + item_name + 'Graphics' + first_dimension + '[' + str(item_size) + '] = { ')
	for x in range(0, item_count):
		graphic_bytes, color_bytes = parse_png(png_name, pixel_width, pixel_height, x * item_width + item_x, item_y, item_width, item_height, alpha_color)
		if item_count > 1:
			f_source.write('\n{ ')
		f_source.write(', '.join(graphic_bytes))
		if item_count > 1:
			f_source.write(' }' + ('' if x == item_count-1 else ',') +'\n')
	f_source.write(' };\n')
	if color_bytes != None:
		f_header.write('\nextern const uint8_t ' + item_name + 'Colu[' + str(len(color_bytes)) + '];\n')
		f_source.write('\nconst uint8_t ' + item_name + 'Colu[' + str(len(color_bytes)) + '] = { ')
		f_source.write(', '.join(color_bytes))
		f_source.write(' };\n')

parse_palette('palette.png')

f_header = open('assets.h', 'wt', newline='\n')
f_header.write('''#ifndef ASSETS_H
#define ASSETS_H
#include <stdint.h>
''')

f_source = open('assets.cpp', 'wt', newline='\n')
f_source.write('#include "assets.h"\n')

png_name = 'title_screen.png'
item_name = 'Title'
graphic_bytes, color_bytes = parse_png(png_name, 1, 2, 0, 0, 1, 192, (0,0,0))
f_header.write('\nextern const uint8_t ' + item_name + 'COLUBK[192];\n')
f_source.write('\nconst uint8_t ' + item_name + 'COLUBK[192] = { ')
f_source.write(', '.join(color_bytes))
f_source.write(' };\n')

parse_sprite_strip(f_header, f_source, 'title_screen.png','TitleGRP', 8, 32, 1, 4, 2, 55, 30, (136,0,0))


f_header.write('\n\n#endif // ASSETS_H')
