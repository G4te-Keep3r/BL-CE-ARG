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
	good = 0
	ret = [] #SEQ-1424, [cordinates 1], [cord2], [cord3], [cord4], [cord5]
	DONE = False
	coordinatesFound = 0
	with open(gif) as f:
		for line in f:
			if not DONE:
				#print '****', line
				if 'Data recovered: SEQ-' in line:
					ret.append(line.split("SEQ-")[1].split("=")[0].strip())
					ret.append(line.split("'")[-2])
				#if 'No SEQ data found at this coordinate' in line: #hope this works-at least 1 of the "coordinate" has another random character "coord[not utf8]inate"
				if 'No SEQ data found at this' in line:
					coordinatesFound += 1
					if coordinatesFound == 3:
						csvPoints = line.split("Scanning")[1].split(": No SEQ data")[0].split(" ")[1]
						csvPoints = csvPoints.split(',')
						ret.append('['+csvPoints[0]+';'+csvPoints[1]+']')
					#points separated by ; and not , so when you open the csv it does not split them
				if line.strip() == 'Fragment data follows...':
					DONE = True
	#return ret
	return good

def investigate_middle(gif):
	#print gif
	foundshort = 0
	foundlong = 0
	ret = [] #SEQ-1424, [cordinates 1], [cord2], [cord3], [cord4], [cord5]
	DONE = False
	coordinatesFound = 0
	with open(gif) as f:
		for line in f:
			if not DONE:
				#print '****', line
				if 'Data recovered: SEQ-' in line:
					ret.append(line.split("SEQ-")[1].split("=")[0].strip())
					ret.append(line.split("'")[-2])
				if 'No SEQ data found at this coordinate' in line: #hope this works-at least 1 of the "coordinate" has another random character "coord[not utf8]inate"
					foundlong += 1
				if 'No SEQ data found at this' in line:
					foundshort += 1
				if line.strip() == 'Fragment data follows...':
					DONE = True
	#return ret
	return [foundlong, foundshort]

def test():
	dl = {}
	ds = {}
	numURLs = 0.0
	with open('urls.txt') as f:
		for line in f:
			numURLs += 1.0
	print 'numURLs:', numURLs
	count = 0.0
	lastper = 0
	perchange = 7 #cause bungie
	with open('urls.txt') as f:
		for line in f:
			out = []
			line = line.strip()
			#print line
			ret = investigate_middle(line.split('/')[-1])
			#long
			if ret[0] not in dl:
				dl[ret[0]] = 0
			dl[ret[0]] += 1

			if ret[1] not in ds:
				ds[ret[1]] = 0
			ds[ret[1]] += 1

			count += 1.0
			if count / numURLs*100.0 > lastper+perchange:
				lastper = count/numURLs*100.0
				print count, str(lastper)+'%'

	print
	print '-'*25
	print
	for k in dl:
		print k, dl[k]
	print
	print '-'*25
	print
	for k in ds:
		print k, ds[k]
	print
	print '-'*25
	print

#1 black
#0 white

def main():
	test()
	return
	#print get_other_data('fragment_v2_e0d3a69c-172c-4d4c-9d15-b4d7094278b5.gif')
	#return
	numURLs = 0.0
	with open('urls.txt') as f:
		for line in f:
			numURLs += 1.0
	print 'numURLs:', numURLs
	count = 0.0
	lastper = 0
	perchange = 7 #cause bungie
	with open('data_1-black_0-white_middle-coord.csv', 'w+') as w:
		with open('urls.txt') as f:
			for line in f:
				out = []
				line = line.strip()
				#r = requests.get(line)#, allow_redirects=True)
				#with open(line.split('/')[-1], 'wb') as gif:
				#	gif.write(r.content)
				#open(line.split('/')[-1], 'wb').write(r.content)
				
				'''all should be downloaded now...'''
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
				#else:
				#	print count

if __name__ == '__main__':
	main()

'''
csv output

name, SEQ-####, value, [cordinates 1], [cord2], [cord3], [cord4], [cord5], "bitstream"
'''