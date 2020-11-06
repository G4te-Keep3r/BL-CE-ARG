import imageio

def makegif(num, count, increment=1): #defaults to every frame
	gif = []
	for i in range(0,count,increment):
		print i
		each_image = imageio.imread("out"+str(num)+"/"+str(i)+".png")
		gif.append(each_image)
	if count%increment != 0: #add the last one at the end
		print i
		each_image = imageio.imread("out"+str(num)+"/"+str(i)+".png")
		gif.append(each_image)

	imageio.mimsave("renders/out-"+str(num)+"_count-"+str(count)+"_increment-"+str(increment)+".gif", gif, 'GIF')

def main():
	maxCount = 26982
	#makegif(4, 6000)
	makegif(6, 22667, 1000)

if __name__ == '__main__':
	main()