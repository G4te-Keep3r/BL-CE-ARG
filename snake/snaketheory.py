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

def trackData(spreadsheet):
    global charlist

    with open(spreadsheet, newline = '\n') as csvfile:

        grid = [[['+']] * 48] * 44

        creader = csv.reader(csvfile, delimiter =',', quotechar = '\'')
        for row in creader:
            char = row[1]

            grid[int(row[2])][int(row[3])].append(char)
            grid[int(row[4])][int(row[5])].append(char)
            grid[int(row[6])][int(row[7])].append(char)
            grid[int(row[8])][int(row[9])].append(char)
            grid[int(row[10])][int(row[11])].append(char)

        for char in charlist:
            for row in grid:
                for point in row:
                    if not char in point:
                        #print(f"Point does not contain {char}")
                        pass

    x = input("Press enter to skip. Enter any character to generate a massive useless .txt file")
    if x != '':
        print("Here it comes...")
        giganticString = '\n\n'.join('\n'.join(' '.join(str(x or '----')for x in y)for y in z)for z in grid)
        f = open("map.txt", "w+")
        f.write(giganticString)
        f.close()

data = input("input filename: ")

readData(data)
trackData("v2_spreadsheet.csv")