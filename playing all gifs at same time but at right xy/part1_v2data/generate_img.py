import numpy as np
import scipy.misc as smp

def make_img(d, i):
	data = np.zeros( (48,44,3), dtype=np.uint8 )

	for cord in d:
		ca = list(cord) #"cord array"
		if len(d[cord]) == 0: #missing data...blue
			data[ca] = [0,0,127]
		elif len(d[cord]) == 2: #conflict...red
			data[ca] = [127,0,0]
		elif d[cord] == 0:
			data[ca] = [255,255,255]
		else: #elif d[cord] == 1:
			data[ca] = [0,0,0]

	img = smp.toimage( data )       # Create a PIL image
	#img.show()                      # View in default viewer
	img.save('out/'+str(i)+'.png')

def main():
	frames = {} #cordinates in order in gif as text
	#for i in range(5):
	#	frames[i] = {} #[x,y] = [values...since there might be conflicts]
	#not range 5, range len(longest bs)

	with open('data_1-black_0-white.csv') as f:
		for line in f:
			print line
			line = line.split(',')
			print line
			bs = line[-1].strip()
			cords = line[3:8]
			for i in range(len(cords)): #in csv file they are ; delimitered, and i need them as a number not string here
				print cords[i]
				cords[i] = [int(cords[i].split(';')[0].split('[')[1]), int(cords[i].split(';')[1].split(']')[0])]

			for i in range(len(bs)):
				bit = int(bs[i])
				if i not in frames:
					frames[i] = {}

				tempcord = tuple(cords[i%5]) #an array cannot be used as an index for a dict as it is not hashable
				if tempcord not in frames[i]:
					frames[i][tempcord] = []
					#i know this is not quite as efficient with the redundant check below, but it makes it a little easier to read and tweak as working on it

				#already conflict if is 2, thus skip anything further
				if len(frames[i][tempcord]) != 2:
					#none saved
					if len(frames[i][tempcord]) == 0:
						frames[i][tempcord].append(bit)
					#same  ---  dont check for, this would be a default case (sorta) but no action is needed
					#if frames[i][tempcord][0] == bit:
					#diff
					if frames[i][tempcord][0] != bit:
						frames[i][tempcord].append(bit)

	#pass frames to generate images
	count = 0.0
	lastper = 0
	perchange = 7 #cause bungie
	for i in range(len(frames)):
		make_img(frames[i], i)
		count += 1.0
		if count / numURLs*100.0 > lastper+perchange:
			lastper = count/numURLs*100.0
			print count, str(lastper)+'%'

'''
##################################
if many conflicts, instead keep count of how many times each is set for each pixel and go with the more common count (or in case of tie still call it a conflict)
##################################
'''

if __name__ == '__main__':
	main()