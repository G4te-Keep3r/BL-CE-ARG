def main():
	longest = 0
	with open('data_1-black_0-white.csv') as f:
		for line in f:
			#print line
			line = line.split(',')
			#print line
			bs = len(line[-1].strip())
			if bs > longest:
				longest = bs
				print
				print '='*25
				print line
				print '='*25
				print

	print longest

if __name__ == '__main__':
	main()