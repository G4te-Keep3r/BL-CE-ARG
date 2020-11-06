import numpy as np
import scipy.misc as smp

#1 black
#0 white
outnum = 6

#frame based, not gif based
#like the pixel itself stays until told to change
lasts = []

data = np.zeros( (48,44,3), dtype=np.uint8 )
for x in range(48):
	for y in range(44):
		data[x,y] = [127,0,255] #purple, not used anywhere else currently

def make_img(d, i):
	for cord in d.keys():
		ca = list(cord) #"cord array"
		#print ca, cord, d[cord]

		#determine winner
		if d[cord] == '': #missing data...silver
			data[ca[0],ca[1]] = [193,193,193]
			####data[ca] = [193,193,193] does a whole row...
		elif d[cord] == 0: #white
			data[ca[0],ca[1]] = [255,255,255]
		elif d[cord] == 1: #black
			data[ca[0],ca[1]] = [0,0,0]
		elif d[cord] == -1: #conflict...red
			data[ca[0],ca[1]] = [255,0,0]

	#if the bs of a gif ended on a spot, it will be set above or made "blank"(/silver) here
	#for cord in lasts:
	#	ca = list(cord) #"cord array"
	#	if tuple(data[ca[0],ca[1]]) == tuple([127,0,255]):
	#		data[ca[0],ca[1]] = [193,193,193]

	img = smp.toimage( data )       # Create a PIL image
	#img.show()                      # View in default viewer
	img.save('out'+str(outnum)+'/'+str(i)+'.png')

'''
purple - initialized canvas
silver - missing data
white - white (0)
black - black (1)
red - conflict of what a data point should be
'''

def main():
	frames = {} #cordinates in order in gif as text
	#for i in range(5):
	#	frames[i] = {} #[x,y] = [values...since there might be conflicts]
	#not range 5, range len(longest bs)

	with open('data_1-black_0-white.csv') as f:
		for line in f:
			#print line
			line = line.split(',')
			#print line
			bs = line[-1].strip()
			cords = line[3:8]
			for i in range(len(cords)): #in csv file they are ; delimitered, and i need them as a number not string here
				#print cords[i]
				cords[i] = [int(cords[i].split(';')[0].split('[')[1]), int(cords[i].split(';')[1].split(']')[0])]
				#for i in cords:
				#	print i
			#print cords

			for i in range(len(bs)): #crashed after that 22667 :(
				bit = int(bs[i])
				if i not in frames:
					frames[i] = {}

				tempcord = tuple(cords[i%5]) #an array cannot be used as an index for a dict as it is not hashable
				if tempcord not in frames[i]:
					frames[i][tempcord] = ''

				if frames[i][tempcord] != bit: #if same we leave it be
					if frames[i][tempcord] == '': #good clean go
						frames[i][tempcord] = bit
					elif frames[i][tempcord] != bit: #-1 or the other bit, redundant but cleaner/shorter code and this doesnt really need to be optimized
						frames[i][tempcord] = -1

	#pass frames to generate images
	count = 0.0
	lastper = 0
	perchange = 7 #cause bungie
	for i in range(len(frames)):
		make_img(frames[i], i)
		count += 1.0
		#26982 is the longest bs string found so far with 848 URLs found
		if count / 26982.0*100.0 > lastper+perchange:
			lastper = count/26982.0*100.0
			print count, str(lastper)+'%'

if __name__ == '__main__':
	main()