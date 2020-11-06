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

def extractFrames(inGif):
	spaceless = ''
	frame = Image.open(inGif)
	nframes = 0
	while frame:
		colorCode = get_main_color(frame)
		if colorCode in [0,1]: #yellow is 2 or 3
			spaceless += str(colorCode)
		nframes += 1
		try:
			frame.seek( nframes )
		except EOFError:
			break;
	return spaceless

def get_other_data(gif):
	ret = [] #SEQ-####, [cordinates 1], [cord2], [cord3], [cord4], [cord5]
	DONE = False
	with open(gif) as f:
		for line in f:
			if not DONE:
				if 'Data recovered: SEQ-' in line:
					ret.append(line.split("SEQ-")[1].split("=")[0].strip())
					value = line.split("'")[-2]
					if value == ',': #i know not great but exporting to a csv so....
						ret.append('comma')
					else:
						ret.append(value)
				if 'No SEQ data found at this' in line:
					csvPoints = line.split("Scanning")[1].split(": No SEQ data")[0].split(" ")[1]
					csvPoints = csvPoints.split(',')
					ret.append('['+csvPoints[0]+';'+csvPoints[1]+']')
					#points separated by ; and not , so when you open the csv it does not split them
				if line.strip() == 'Fragment data follows...':
					DONE = True
	return ret

#1 black
#0 white

def main():
	numURLs = 0.0
	with open('urls.txt') as f:
		for line in f:
			numURLs += 1.0
	print 'numURLs:', numURLs
	count = 0.0
	lastper = 0
	perchange = 7 #cause bungie
	with open('data_1-black_0-white.csv', 'w+') as w:
		with open('urls.txt') as f:
			for line in f:
				out = []
				line = line.strip()

				'''need to make this check instead of redownload...'''
				urllib.urlretrieve(line, line.split('/')[-1])
				out.append(line.split('/')[-1])
				out.extend(get_other_data(line.split('/')[-1]))
				out.append(extractFrames(line.split('/')[-1]))

				w.write(', '.join(out))
				w.write('\n')
				count += 1.0
				if count / numURLs*100.0 > lastper+perchange:
					lastper = count/numURLs*100.0
					print count, str(lastper)+'%'

if __name__ == '__main__':
	main()

'''
csv output

name, SEQ-####, value, [cordinates 1], [cord2], [cord3], [cord4], [cord5], "bitstream"
'''