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
	print extractFrames('fragment_e679ed2a-b11f-4f89-b25f-7aac559ea0a0.gif')
	return
	count = 0.0
	lastper = 0
	perchange = 7 #cause bungie
	with open('data.csv', 'w+') as w:
		with open('urls.txt') as f:
			for line in f:
				out = []
				line = line.strip()
				#r = requests.get(line)#, allow_redirects=True)
				#with open(line.split('/')[-1], 'wb') as gif:
				#	gif.write(r.content)
				#open(line.split('/')[-1], 'wb').write(r.content)
				
				'''all should be downloaded now...'''
				#urllib.urlretrieve(line, line.split('/')[-1])
				out.append(line.split('/')[-1])
				out.extend(get_other_data(line.split('/')[-1]))
				out.append(extractFrames(line.split('/')[-1]))
				#print extractFrames(line.split('/')[-1])
				w.write(', '.join(out))
				w.write('\n')
				count += 1.0
				if count / 1224.0*100.0 > lastper+perchange:
					lastper = count/1224.0*100.0
					print count, str(lastper)+'%'
				else:
					print count

if __name__ == '__main__':
	main()

'''
csv output

name, SEQ-1424, [cordinates 1], [cord2], [cord3], [cord4], [cord5], "bitstream"
'''