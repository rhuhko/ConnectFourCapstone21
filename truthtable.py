# Author: Ruslan Huhko
# For: CS Capstone - Fall 2021
# Advisor: Dr. Michael J Reale
# Creates the Truth Table for a standard 6x7 ConnectFour Game
# Returns Truth Table
# Checks for Win
# Truth Table Layout:
# 0  1  2  3  4  5  6
# 7  8  9  10 11 12 13
# 14 15 16 17 18 19 20
# 21 22 23 24 25 26 27
# 28 29 30 31 32 33 34
# 35 36 37 38 39 40 41

import numpy as np


class TruthTable:

    def __init__(self):
        # Main constructor method
        filename = "truthTable"
        self.truthtable = open(filename, "w")
        self.gameboard = np.arange(42).reshape(6, 7)

        self.trutharray = []
        self.createtable()
        self.truthtable.close()
        self.sortTruthTable()

        self.trutharray = np.array(self.trutharray)

    def returntruthtable(self):
        # Returns truth table
        return self.trutharray

    def returngameboard(self):
        return self.gameboard

    def writetruthtable(self, combination):
        self.truthtable.writelines(str(combination))
        self.truthtable.writelines('\n')
        self.trutharray.append(combination)
        return

    def sortTruthTable(self):
        for i in range(len(self.trutharray)):
            combination = self.trutharray[i].tolist()
            combination.sort(reverse=True)
            self.trutharray[i] = combination
        return

    def horizontalvertical(self):
        # all horizontal positions
        for r in range(6):
            for c in range(4):
                truevalue = self.gameboard[r, c:(c + 4)]
                #truevalue[::-1].sort()
                self.writetruthtable(truevalue)
        # all vertical positions
        for r in range(3):
            for c in range(7):
                truevalue = self.gameboard[r:(r + 4), c]
                #truevalue[::-1].sort()
                self.writetruthtable(truevalue)
        return

    def diagonal(self):
        # positive diagonal truth values
        templist = []
        for r in range(3):
            for c in range(4):
                for i in range(4):
                    truepos = self.gameboard[(r + 3 - i), (c + i)]
                    templist.append(truepos)
                #templist.sort()
                #templist.reverse()
                self.writetruthtable(np.array(templist))
                templist.clear()
        # negative
        for r in range(3):
            for c in range(4):
                for i in range(4):
                    truepos = self.gameboard[(r + i), (c + i)]
                    templist.append(truepos)
                #templist.sort()
                #templist.reverse()
                self.writetruthtable(np.array(templist))
                templist.clear()
        return

    def createtable(self):
        self.horizontalvertical()
        self.diagonal()
        return

    def printtruthtable(self):
        print(self.trutharray)
        return

    def checkwin(self, gameboard):
        # checks win
        # does not use truth table
        templist = []

        # all horizontal positions
        for r in range(6):
            for c in range(4):
                horizontal = gameboard[r, c:(c + 4)]
                #print(horizontal)
                isalpha = True
                for i in horizontal:
                    if not i.isalpha():
                        isalpha = False
                        break
                if not isalpha:
                    continue
                if all(hor == horizontal[0] for hor in horizontal):
                    return True, horizontal[0]

        # all vertical positions
        for r in range(3):
            for c in range(7):
                vertical = gameboard[r:(r + 4), c]
                #print(vertical)
                isalpha = True
                for i in vertical:
                    if not i.isalpha():
                        isalpha = False
                        break
                if not isalpha:
                    continue
                if all(ver == vertical[0] for ver in vertical):
                    return True, vertical[0]

        # positive diagonal
        for r in range(3):
            for c in range(4):
                for i in range(4):
                    truepos = gameboard[(r + 3 - i), (c + i)]
                    templist.append(str(truepos))
                    positive = np.array(templist)
                #print(positive)
                isalpha = True
                for i in positive:
                    if not i.isalpha():
                        isalpha = False
                        break
                if not isalpha:
                    templist.clear()
                    continue
                if all(pos == positive[0] for pos in positive):
                    return True, positive[0]
                templist.clear()

        # negative diagonal
        for r in range(3):
            for c in range(4):
                for i in range(4):
                    truepos = gameboard[(r + i), (c + i)]
                    templist.append(str(truepos))
                    negative = np.array(templist)
                #print(negative)
                isalpha = True
                for i in negative:
                    if not i.isalpha():
                        isalpha = False
                        break
                if not isalpha:
                    templist.clear()
                    continue
                if all(neg == negative[0] for neg in negative):
                    return True, negative[0]
                templist.clear()

        return False, None
