# Author: Ruslan Huhko
# For: CS Capstone - Fall 2021
# Advisor: Dr. Michael J Reale
# Creates/ Accesses Virtual Gameboard
# Returns win

import numpy as np
import truthtable


class GameBoard:

    def __init__(self):
        initarray = np.zeros([6, 7], dtype=int)
        for c in range(initarray.shape[1]):
            for r in range(initarray.shape[0]):
                initarray[r, c] = c

        self.gameboard = initarray.astype(str)
        self.truth = truthtable.TruthTable()

    def recordMove(self, player, column):
        # places chip in bottom-most row within given column

        # If input is just either R, or Y
        if isinstance(player, str):
            for i in reversed(range(self.gameboard.shape[0])):
                if self.gameboard[i, column].isalpha():
                    if i == 0:
                        # Raises Error if the selected column is full
                        raise ValueError
                    else:
                        continue
                else:
                    self.gameboard[i, column] = player
                    break
        else:
            # If input is object of class player
            for i in reversed(range(self.gameboard.shape[0])):
                if self.gameboard[i, column].isalpha():
                    if i == 0:
                        # Raises Error if the selected column is full
                        raise ValueError
                    else:
                        continue
                else:
                    self.gameboard[i, column] = player.playercolor
                    break
        return

    def checkTie(self):
        for r in range(6):
            for c in range(7):
                if not self.gameboard[r, c].isalpha():
                    return False, None
        return True, None

    def checkWin(self):
        # Check for Win
        win, player = self.truth.checkwin(self.gameboard)

        # Check for Tie
        if not win:
            win, player = self.checkTie()

        return win, player

    def printGame(self):
        # Prints current progress of game
        print(self.gameboard)
        return

    def printTruth(self):
        self.truth.printtruthtable()
        return
