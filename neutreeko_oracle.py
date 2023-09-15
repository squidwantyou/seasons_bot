#!/usr/bin/env python
import sys,os


class Move:
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    z1 = 0
    prev = None

def readint(question):
    done = False
    while not done:
        try:
            s = int(input(question))
            done = True
        except ValueError:
            print("Illegal format! Enter an integer")
    return(s)

print("\nNeutreeko (c) 2001, 2002 J K Haugland")
print("\nEnter 0 for standard Neutreeko")
print("\nOtherwise, enter board size:")
width = 0
height = 0
ruleset = 0
while width < 3 or width > 7:
    width = readint("Width = ")
    if width == 0:
        width = 5
        height = 5
        ruleset = 1
        print("\nWidth = 5")
        print("Height = 5")
        print("Winning condition: three in a row, orthogonally or diagonally")
    if width < 3:
        print("Too narrow")
    if width > 7:
        print("Too wide")
while height < 3 or height > 7:
    height = readint("Height = ")
    if height < 3:
        print("Too low")
    if height > 7:
        print("Too high")
if ruleset == 0:
    print("")
while ruleset < 1 or ruleset > 5 or (ruleset == 3 and (width == 3 or height == 3)) or (ruleset == 4 and width < 5 and height < 5) or (ruleset == 5 and (width % 2 == 0 or height % 2 == 0 or width * height < 25)):
    print("Enter winning condition:")
    print("1 = three in a row, orthogonally or diagonally")
    print("2 = three in a row, orthogonally")
    if width > 3 and height > 3:
        print("3 = three in a row, diagonally") # width or height = 3 would make it possible to be trapped with no legal moves
    if width > 4 or height > 4:
        print("4 = three in a straight line, any equidistant") # either width or height must be greater than 3 to make this distinct from no. 1
    if (width == 5 or width == 7) and (height == 5 or height == 7):
        print("5 = occupy the centre") # only possible when width and height are odd - also cf. no. 3
    ruleset = readint("")
if width == height:
    numberOfSymmetries = 8
else:
    numberOfSymmetries = 4
numberOfCells = width * height
numberOfPositions = (numberOfCells * (numberOfCells - 1) * (numberOfCells - 2)) // 6
print("\nCounting positions...")
drawPosition = 500 # just a code; should be set higher than the maximal depth
illegalPosition = 600 # also just a code
indexFromPosition = [[[0 for x in range(numberOfCells)] for y in range(numberOfCells)] for z in range(numberOfCells)]
positionFromIndex = [[0 for x in range(4)] for y in range(numberOfPositions)]
position1col = [[[0 for x in range(height)] for y in range(width)] for z in range(numberOfPositions)]
completedWin = [0 for x in range(numberOfPositions)]
position2col = [[0 for x in range(height)] for y in range(width)]
remainingMoves = [[drawPosition for x in range(numberOfPositions)] for y in range(numberOfPositions)]
moveInformation = [[0 for x in range(6)] for y in range(25)]
movePermutation = [0 for x in range(25)]
symmetry = [[0 for x in range(numberOfSymmetries)] for y in range(numberOfCells)]
piece = ["o", " ", "x"]
choice = ["" for x in range(25)]
for a in range(numberOfCells):
    b = a % width
    c = a // width
    symmetry[a][0] = a
    symmetry[a][1] = (width - 1 - b) + width * c
    symmetry[a][2] = b + width * (height - 1 - c)
    symmetry[a][3] = (width - 1 - b) + width * (height - 1 - c)
    if numberOfSymmetries == 8:
        symmetry[a][4] = c + width * b
        symmetry[a][5] = (width - 1 - c) + width * b
        symmetry[a][6] = c + width * (width - 1 - b)
        symmetry[a][7] = (width - 1 - c) + width * (width - 1 - b)
d = -1
for a in range(numberOfCells - 2):
    for b in range(a + 1, numberOfCells - 1):
        for c in range(b + 1, numberOfCells):
            d += 1
            for e in range(width):
                for f in range(height):
                    position1col[d][e][f] = 0
            position1col[d][a % width][a // width] = 1
            position1col[d][b % width][b // width] = 1
            position1col[d][c % width][c // width] = 1
            completedWin[d] = 0
            if ruleset == 5:
                if a == (numberOfCells - 1) // 2 or b == (numberOfCells - 1) // 2 or c == (numberOfCells - 1) // 2:
                    completedWin[d] = 1
            else:
                if (a % width) + (c % width) == 2 * (b % width) and (a // width) + (c // width) == 2 * (b // width):
                    if (a % width) - (c % width) <= 2 and (c % width) - (a % width) <= 2 and (a // width) - (c // width) <= 2 and (c // width) - (a // width) <= 2:
                        completedWin[d] = 1
                if ruleset == 2 and (a % width) != (c % width) and (a // width) != (c // width):
                    completedWin[d] = 0
                if ruleset == 3 and ((a % width) == (c % width) or (a // width) == (c // width)):
                    completedWin[d] = 0
                if (a % width) + (c % width) == 2 * (b % width) and (a // width) + (c // width) == 2 * (b // width) and ruleset == 4:
                    completedWin[d] = 1
            indexFromPosition[a][b][c] = d
            indexFromPosition[a][c][b] = d
            indexFromPosition[b][a][c] = d
            indexFromPosition[b][c][a] = d
            indexFromPosition[c][a][b] = d
            indexFromPosition[c][b][a] = d
            positionFromIndex[d][0] = a
            positionFromIndex[d][1] = b
            positionFromIndex[d][2] = c
            positionFromIndex[d][3] = 2
for a in range(numberOfPositions):
    for b in range(1, numberOfSymmetries):
        if positionFromIndex[a][3] == 1:
            positionFromIndex[a][3] = 2
        c = 0
        while c < numberOfCells and positionFromIndex[a][3] == 2:
            if position1col[a][c % width][c // width] != position1col[a][symmetry[c][b] % width][symmetry[c][b] // width]:
                if position1col[a][c % width][c // width] == 1:
                    positionFromIndex[a][3] = 1
                else:
                    positionFromIndex[a][3] = 0
            c += 1
        if positionFromIndex[a][3] == 2:
            positionFromIndex[a][3] = 1
j = 0
for a in range(numberOfPositions):
    for b in range(numberOfPositions):
        if completedWin[b] == 1:
            remainingMoves[a][b] = 0
        if completedWin[a] == 1:
            remainingMoves[a][b] = illegalPosition
        if position1col[a][positionFromIndex[b][0] % width][positionFromIndex[b][0] // width] == 1 or position1col[a][positionFromIndex[b][1] % width][positionFromIndex[b][1] // width] == 1 or position1col[a][positionFromIndex[b][2] % width][positionFromIndex[b][2] // width] == 1:
            remainingMoves[a][b] = illegalPosition
        if remainingMoves[a][b] == 0:
            j += 1
            if (j % 100000 == 0):
                print("-", end = "")
print("0 ", j)
c = 1
while j > 0:
    j = 0
    for a in range(numberOfPositions):
        if positionFromIndex[a][3] == 1:
            for b in range(numberOfPositions):
                if remainingMoves[a][b] == drawPosition:
                    stopped = False
                    for k in range(3):
                        d = positionFromIndex[a][k] % width
                        e = positionFromIndex[a][k] // width
                        for f in range(-1, 2):
                            for g in range(-1, 2):
                                if f * f + g * g > 0 and d + f >= 0 and d + f < width and e + g >= 0 and e + g < height and position1col[a][d + f][e + g] == 0 and position1col[b][d + f][e + g] == 0 and not stopped:
                                    f1 = f
                                    g1 = g
                                    while d + f1 + f >= 0 and d + f1 + f < width and e + g1 + g >= 0 and e + g1 + g < height and position1col[a][d + f1 + f][e + g1 + g] == 0 and position1col[b][d + f1 + f][e + g1 + g] == 0:
                                        f1 += f
                                        g1 += g
                                    for h in range(3):
                                        movePermutation[h] = positionFromIndex[a][h]
                                    movePermutation[k] = d + f1 + width * (e + g1)
                                    h = indexFromPosition[movePermutation[0]][movePermutation[1]][movePermutation[2]]
                                    if c % 2 == 0:
                                        if remainingMoves[b][h] < c:
                                            remainingMoves[a][b] = c
                                        else:
                                            remainingMoves[a][b] = drawPosition
                                            stopped = True
                                    else:
                                        if remainingMoves[b][h] == c - 1:
                                            remainingMoves[a][b] = c
                                            stopped = True
                    if remainingMoves[a][b] == c:
                        j += 1
                        if j % 100000 == 0:
                            print("-", end = "")
                        for d in range(1, numberOfSymmetries):
                            e = indexFromPosition[symmetry[positionFromIndex[a][0]][d]][symmetry[positionFromIndex[a][1]][d]][symmetry[positionFromIndex[a][2]][d]]
                            f = indexFromPosition[symmetry[positionFromIndex[b][0]][d]][symmetry[positionFromIndex[b][1]][d]][symmetry[positionFromIndex[b][2]][d]]
                            if remainingMoves[e][f] != c:
                                remainingMoves[e][f] = c
                                j += 1
                                if j % 100000 == 0:
                                    print("-", end = "")
    print(str(c) + "  " + str(j))
    c += 1
for a in range(numberOfPositions):
    for b in range(numberOfPositions):
        if remainingMoves[a][b] == drawPosition:
            j += 1
print("\nNumber of draws:", j)
print("\nDeepest position(s):")
for a in range(numberOfPositions):
    if positionFromIndex[a][3] == 1:
        for b in range(numberOfPositions):
            if remainingMoves[a][b] == c - 2:
                pos1 = "x -"
                for d in range(3):
                    pos1 += " " + chr(positionFromIndex[a][d] % width + 65) + str(1 + positionFromIndex[a][d] // width)
                pos1 += "   o -"
                for d in range(3):
                    pos1 += " " + chr(positionFromIndex[b][d] % width + 65) + str(1 + positionFromIndex[b][d] // width)
                print(pos1)
if (width == 5 or width == 7) and height == width and (ruleset == 1 or ruleset == 5):
    if ruleset == 1:
        a = indexFromPosition[(width - 3) // 2][(width + 1) // 2][(numberOfCells - 1) // 2 + width]
        b = indexFromPosition[(numberOfCells - 1) // 2 - width][numberOfCells - (width + 3) // 2][numberOfCells - (width - 1) // 2]
    else:
        a = indexFromPosition[(numberOfCells - 1) // 2 - 2 * width][(numberOfCells - 1) // 2 + width - 2][(numberOfCells - 1) // 2 + width + 2]
        b = indexFromPosition[(numberOfCells - 1) // 2 - width - 2][(numberOfCells - 1) // 2 - width + 2][(numberOfCells - 1) // 2 + 2 * width]
else:
    print("\n(This may not be a suitable opening position)")
    a = indexFromPosition[0][2][numberOfCells - 2]
    b = indexFromPosition[1][numberOfCells - 3][numberOfCells - 1]
for c in range(width):
    for d in range(height):
        position2col[c][d] = position1col[a][c][d] - position1col[b][c][d]
mv = Move()
stripe = "\n +"
for c in range(width):
    stripe += "---+"
while remainingMoves[a][b] > 0:
    print(stripe)
    for d in range(height):
        pos1 = str(height - d) + "|"
        for c in range(width):
            pos1 += " " + piece[1 + position2col[c][height - 1 - d]] + " |"
        print(pos1 + stripe)
    pos1 = ""
    for c in range(width):
        pos1 += "   " + chr(c + 65)
    print(pos1 + "\n")
    j = 0
    if remainingMoves[a][b] == illegalPosition:
        print("Illegal position")
    else:
        for k in range(3):
            d = positionFromIndex[a][k] % width
            e = positionFromIndex[a][k] // width
            for f in range(-1, 2):
                for g in range(-1, 2):
                    if f * f + g * g > 0 and d + f >= 0 and d + f < width and e + g >= 0 and e + g < height and position2col[d + f][e + g] == 0:
                        f1 = f
                        g1 = g
                        while d + f1 + f >= 0 and d + f1 + f < width and e + g1 + g >= 0 and e + g1 + g < height and position2col[d + f1 + f][e + g1 + g] == 0:
                            f1 += f
                            g1 += g
                        for h in range(3):
                            movePermutation[h] = positionFromIndex[a][h]
                        movePermutation[k] = d + f1 + width * (e + g1)
                        h = indexFromPosition[movePermutation[0]][movePermutation[1]][movePermutation[2]]
                        j += 1
                        choice[j] = ". " + chr(d + 65) + str(e + 1) + " -> " + chr(d + f1 + 65) + str(e + g1 + 1) + " : "
                        if remainingMoves[b][h] == drawPosition:
                            choice[j] += "Draw"
                        else:
                            if remainingMoves[b][h] % 2 == 0:
                                choice[j] += "Win"
                            else:
                                choice[j] += "Loss"
                            if remainingMoves[b][h] > 0:
                                choice[j] += " in " + str(remainingMoves[b][h] + 1) + " moves"
                        moveInformation[j][0] = d
                        moveInformation[j][1] = e
                        moveInformation[j][2] = d + f1
                        moveInformation[j][3] = e + g1
                        moveInformation[j][4] = h
                        moveInformation[j][5] = remainingMoves[b][h]
                        if moveInformation[j][5] % 2 == 0:
                            moveInformation[j][5] -= drawPosition
                        else:
                            moveInformation[j][5] = drawPosition - moveInformation[j][5]
    for c in range(1, j + 1):
        movePermutation[c] = c
    for c in range(1, j):
        for d in range(c + 1, j + 1):
            if moveInformation[movePermutation[c]][5] > moveInformation[movePermutation[d]][5]:
                e = movePermutation[c]
                movePermutation[c] = movePermutation[d]
                movePermutation[d] = e
    for c in range(1, j + 1):
        print(str(c) + choice[movePermutation[c]])
    if mv.prev != None:
        print("77. Retract last move")
    if (width == 5 or width == 7) and height == width and (ruleset == 1 or ruleset == 5):
        print("88. Back to start")
    print("99. Enter new position")
    d = 98
    while d != 99 and (d < 1 or d > j) and (d != 88 or (width != 5 and width != 7) or height != width or (ruleset != 1 and ruleset != 5)) and (d != 77 or mv.prev == None):
        d = readint("Enter alternative: ")
    if d == 77:
        b = a
        a = mv.z1
        for c in range(width):
            for d in range(height):
                position2col[c][d] = -position2col[c][d]
        piece[1] = piece[0]
        piece[0] = piece[2]
        piece[2] = piece[1]
        piece[1] = " "
        position2col[mv.x1][mv.y1] = 1
        position2col[mv.x2][mv.y2] = 0
        mv = mv.prev
    else:
        if d == 88:
            if ruleset == 1:
                a = indexFromPosition[(width - 3) // 2][(width + 1) // 2][(numberOfCells - 1) // 2 + width]
                b = indexFromPosition[(numberOfCells - 1) // 2 - width][numberOfCells - (width + 3) // 2][numberOfCells - (width - 1) // 2]
            else:
                a = indexFromPosition[(numberOfCells - 1) // 2 - 2 * width][(numberOfCells - 1) // 2 + width - 2][(numberOfCells - 1) // 2 + width + 2]
                b = indexFromPosition[(numberOfCells - 1) // 2 - width - 2][(numberOfCells - 1) // 2 - width + 2][(numberOfCells - 1) // 2 + 2 * width]
            for c in range(width):
                for d in range(height):
                    position2col[c][d] = position1col[a][c][d] - position1col[b][c][d]
            piece[0] = "o"
            piece[1] = " "
            piece[2] = "x"
            mv = Move()
        else:
            if d == 99:
                h1 = 0
                h2 = 0
                h3 = 0
                while h1 != numberOfCells - 6 or h2 != 3 or h3 != 3:
                    print("Enter one "+ str(width) + "-digit number for each row")
                    print("0 = blank; 1 = 'x' (plays first); 2 = 'o'")
                    print("(The input is read as an integer, and starting zeros can be omitted)")
                    for e in range(width):
                        for f in range(height):
                            position2col[e][f] = 0
                    for e in range(height):
                        f = readint("")
                        for g in range(width):
                            position2col[width - 1 - g][height - 1 - e] = f % 10
                            f = f // 10
                        for f in range(width):
                            if position2col[f][height - 1 - e] == 2:
                                position2col[f][height - 1 - e] = -1
                    h1 = 0
                    h2 = 0
                    h3 = 0
                    for e in range(width):
                        for f in range(height):
                            if position2col[e][f] == 0:
                                h1 += 1
                            if position2col[e][f] == 1:
                                h2 += 1
                            if position2col[e][f] == -1:
                                h3 += 1
                    if h1 != numberOfCells - 6:
                        print("Error: " + str(h1) + " blanks (should be " + str(numberOfCells - 6) + ")")
                    if h2 != 3:
                        print("Error: " + str(h2) + " x's (should be 3)")
                    if h3 != 3:
                        print("Error: " + str(h3) + " o's (should be 3)")
                h1 = 0
                while position2col[h1 % width][h1 // width] <= 0:
                    h1 += 1
                h2 = h1 + 1
                while position2col[h2 % width][h2 // width] <= 0:
                    h2 += 1
                h3 = h2 + 1
                while position2col[h3 % width][h3 // width] <= 0:
                    h3 += 1
                a = indexFromPosition[h1][h2][h3]
                h1 = 0
                while position2col[h1 % width][h1 // width] >= 0:
                    h1 += 1
                h2 = h1 + 1
                while position2col[h2 % width][h2 // width] >= 0:
                    h2 += 1
                h3 = h2 + 1
                while position2col[h3 % width][h3 // width] >= 0:
                    h3 += 1
                b = indexFromPosition[h1][h2][h3]
                piece[0] = "o"
                piece[1] = " "
                piece[2] = "x"
                mv = Move()
            else:
                c = movePermutation[d]
                mv2 = Move()
                mv2 = mv
                mv = Move()
                mv.prev = mv2
                mv.x1 = moveInformation[c][0]
                mv.y1 = moveInformation[c][1]
                mv.x2 = moveInformation[c][2]
                mv.y2 = moveInformation[c][3]
                mv.z1 = a
                a = b
                b = moveInformation[c][4]
                position2col[moveInformation[c][0]][moveInformation[c][1]] = 0
                position2col[moveInformation[c][2]][moveInformation[c][3]] = 1
                for c in range(width):
                    for d in range(height):
                        position2col[c][d] = -position2col[c][d]
                piece[1] = piece[0]
                piece[0] = piece[2]
                piece[2] = piece[1]
                piece[1] = " "
print(stripe)
for d in range(height):
    pos1 = str(height - d) + "|"
    for c in range(width):
        pos1 += " " + piece[1 + position2col[c][height - 1 - d]] + " |"
    print(pos1 + stripe)
pos1 = ""
for c in range(width):
    pos1 += "   " + chr(c + 65)
print(pos1 + "\n\nGAME OVER\n")
