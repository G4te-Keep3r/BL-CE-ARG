import os
from PIL import Image
import urllib

def get_main_color(img):#file):
	#img = Image.open(file)
	colors = img.getcolors(256) #put a higher value if there are many colors in your image
	max_occurence, most_present = 0, 0
	try:
		for c in colors:
			if c[0] > max_occurence:
				(max_occurence, most_present) = c
		return most_present
	except TypeError:
		raise Exception("Too many colors in the image")

#def extractFrames(inGif, outFolder):
def extractFrames(inGif):
	#ycount = 0
	spaceless = ''
	frame = Image.open(inGif)
	return get_main_color(frame)
	nframes = 0
	while frame:
		print get_main_color(frame),
		#frame.save( '%s/%s-%s.gif' % (outFolder, os.path.basename(inGif), nframes ) , 'GIF')
		colorCode = get_main_color(frame)
		#if colorCode == 3: #yellow
		#	ycount += 1
		#	colorCode = '' #go back and make sure there is only ever 1 yellow
		#if colorCode == 1: #black
		#	colorCode = 'b'
		#else: #white
		#	colorCode = 'w'
		#colorCode = str(colorCode)
		if colorCode != 3:
			spaceless += str(colorCode)
		nframes += 1
		try:
			frame.seek( nframes )
		except EOFError:
			break;
	#if ycount > 1:
	#	print '*'*25
	#	print ycount, inGif
	return spaceless

def get_other_data(gif):
	ret = [] #SEQ-1424, [cordinates 1], [cord2], [cord3], [cord4], [cord5]
	DONE = False
	with open(gif) as f:
		for line in f:
			if not DONE:
				if 'Data recovered: SEQ-13685' in line:
					ret.append(line.split("'")[-2])
				if 'No SEQ data found at this coordinate' in line:
					ret.append('['+line.split("Scanning")[1].split(": No SEQ data")[0].split(" ")[1]+']')
				if line.strip() == 'Fragment data follows...':
					DONE = True
	return ret

#extractFrames('fragment_a682843d-43a2-4dd0-a4d7-abfddee4a61d.gif', 'output')

#1 black
#0 white

def main():
	y2 = 0
	y3 = 0
	with open('urls.txt') as f:
		for line in f:
			line = line.strip()
			if extractFrames(line.split('/')[-1]) == 2:
				y2 += 1
			elif extractFrames(line.split('/')[-1]) == 3:
				y3 += 1
			else:
				print '*'*5, extractFrames(line.split('/')[-1])
	print
	print
	print 'y2', y2
	print 'y3', y3

if __name__ == '__main__':
	main()

'''
csv output

name, SEQ-1424, [cordinates 1], [cord2], [cord3], [cord4], [cord5], "bitstream"
'''