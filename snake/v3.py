from prettytable import PrettyTable
import csv

charlist = []

def readData(file):
	f = open(file,"r")
	lines = f.readlines()
	global charlist
	csvstring = ''
	row = ''
	for line in lines:
		# Data Headers
		if line.startswith("Data"):
			if row != '':
				csvstring = csvstring + row + "\n"
			row = ''
			x = line.strip("\n")
			x = x.split("SEQ-")[1]
			#number
			num = x.split(" = ")[0]

			#character
			char = x.split(" = ")[1]
			if char == '\',\'':
				char = 'comma'
			else:
				char = char.split("'")[1]
				#char = char.strip()
			if char not in charlist:
					charlist.append(char)


			row = num + "," + char

		# Coordinate Scanning
		else:
			x = line.split("Scanning ")[1]
			x = x.split(": No")[0]
			#print(x)
			row = row + "," + x
	f.close()

	f = open("v2_spreadsheet.csv", "w+")
	f.write(csvstring)
	f.close()
	print("Spreadsheet created")
	print(f)
	#print charlist
	#print charlist[2]

def trackData(spreadsheet):
	global charlist
	d = {} #d[x][y] ==> [48][44]
	for x in range(48):
		d[x] = {}
		for y in range(44):
			d[x][y] = []
			for c in charlist:
				d[x][y].append(c) #this is to help avoid the weird pointer errors you can sometimes run into

	hasBeenRemoved = []

	with open(spreadsheet) as csvfile:

		#grid = [[['+']] * 48] * 44

		creader = csv.reader(csvfile, delimiter =',', quotechar = '\'')
		for row in creader:
			#print '**', row, '**'
			char = row[1]

			for pointMultiplier in range(1,6):
				#i know x&y do not need to be explicity defined, but makes it easier to read and easier to do more things with them if need be l8r
				x = int(row[2*pointMultiplier])
				y = int(row[(2*pointMultiplier)+1])
				if char in d[x][y]:
					d[x][y].remove(char)
					#print x, y, char
					if char not in hasBeenRemoved:
						hasBeenRemoved.append(char)
				elif char not in hasBeenRemoved:
					print '', '', 'XXX', x, y, char

	x_lables = ['']
	x_lables.extend(range(0,48))
	t = PrettyTable(x_lables)
	for y in range(44):
		row = [y]
		for x in range(48):
			row.append(d[x][y])
		t.add_row(row)
	#print t
	t_text = t.get_string() #save to file
	with open('table.txt', 'w+') as w:
		w.write(t_text)


	x_lables = ['']
	x_lables.extend(range(0,48))
	t = PrettyTable(x_lables)
	for y in range(44):
		row = [y]
		for x in range(48):
			numRemoved = len(charlist) - len(d[x][y])
			if numRemoved == 0:
				row.append('')
			else:
				row.append(numRemoved)
		t.add_row(row)
	#print t
	t_text = t.get_string() #save to file
	with open('table_numRemoved.txt', 'w+') as w:
		w.write(t_text)

	return

	#x = input("Press enter to skip. Enter any character to generate a massive useless .txt file")
	if True:#x != '':
		print("Here it comes...")
		giganticString = '\n\n'.join('\n'.join(' '.join(str(x or '----')for x in y)for y in z)for z in grid)
		f = open("map.txt", "w+")
		f.write(giganticString)
		f.close()

def main():
	#commented out so i can run it in sublime and not have to open cmd/terminal
	'''
	data = input("input filename: [enter for lines.txt]")

	if data == '':
		data = 'lines.txt'
	'''
	data = 'lines.txt'

	readData(data)
	#save charlist as own thing so can run trackData without having to reparse data
	trackData("v2_spreadsheet.csv")

if __name__ == '__main__':
	main()