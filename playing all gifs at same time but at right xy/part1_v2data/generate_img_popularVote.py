import numpy as np
import scipy.misc as smp

def make_img(d, i):
	data = np.zeros( (48,44,3), dtype=np.uint8 )

	for cord in d:
		ca = list(cord) #"cord array"
		print ca, cord, d[cord]

		#determine winner
		if (d[cord][0] + d[cord][1]) == 0: #missing data...blue
			data[ca] = [0,0,127]
		elif d[cord][0] > d[cord][1]:
			data[ca] = [255,255,255]
		elif d[cord][0] < d[cord][1]:
			data[ca] = [0,0,0]
		elif d[cord][0] == d[cord][1]: #conflict...red
			data[ca] = [127,0,0]

	img = smp.toimage( data )       # Create a PIL image
	#img.show()                      # View in default viewer
	#img.save('out2/'+str(i)+'.png')

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
			print cords

			for i in range(len(bs)):
				bit = int(bs[i])
				if i not in frames:
					frames[i] = {}

				tempcord = tuple(cords[i%5]) #an array cannot be used as an index for a dict as it is not hashable
				if tempcord not in frames[i]:
					frames[i][tempcord] = [0,0]

				frames[i][tempcord][bit] += 1

	#pass frames to generate images
	count = 0.0
	lastper = 0
	perchange = 7 #cause bungie
	for i in [0]:#range(len(frames)):
		make_img(frames[i], i)
		count += 1.0
		#26982 is the longest bs string found so far with 848 URLs found
		if count / 26982.0*100.0 > lastper+perchange:
			lastper = count/26982.0*100.0
			print count, str(lastper)+'%'

if __name__ == '__main__':
	main()