# Author: Ruslan Huhko
# For: CS Capstone - Fall 2021
# Advisor: Dr. Michael J Reale
# Play Ball
# Queries User/ AI for next position

import gameboard
import player
import algorithms


class Play:

    def __init__(self):
        self.game = gameboard.GameBoard()
        self.algorithm = algorithms.Algorithm(self.game.gameboard)
        self.winner = player.Player(None)
        self.player1 = player.Player('R')  # Red, counter 0
        self.player2 = player.Player('Y')  # Yellow, counter 1
        self.win = False
        self.playercounter = 0

    def getNextMove(self):
        # Designed for mortals

        try:
            self.game.printGame()
            if (self.playercounter % 2) == 0:
                print("Player ", str(self.player1.playercolor), ": Select Column Number:")
                selection = int(input())
                self.playercounter += 1
                self.game.recordMove(self.player1, selection)
            elif (self.playercounter % 2) == 1:
                print("Player ", str(self.player2.playercolor), ": Select Column Number:")
                selection = int(input())
                self.playercounter += 1
                self.game.recordMove(self.player2, selection)
            self.win, winner = self.game.checkWin()
        except ValueError:
            print("Invalid Move!")
            exit()

        if self.win:
            if winner == self.player1.playercolor:
                self.winner = self.player1
            if winner == self.player2.playercolor:
                self.winner = self.player2

    def random(self):
        # Calls the algorithm bruteForce method, and sends current gameboard
        # to prevent selecting unavailable position

        try:
            if (self.playercounter % 2) == 0:
                selection = int(self.algorithm.random())
                self.playercounter += 1
                self.game.recordMove(self.player1, selection)
            elif (self.playercounter % 2) == 1:
                selection = int(self.algorithm.random())
                self.playercounter += 1
                self.game.recordMove(self.player2, selection)
            self.win, winner = self.game.checkWin()
        except ValueError:
            print('Invalid Move!')
            exit()

        if self.win:
            if winner == self.player1.playercolor:
                self.winner = self.player1
            if winner == self.player2.playercolor:
                self.winner = self.player2

    def bruteForce(self):
        try:
            if (self.playercounter % 2) == 0:
                selection = int(self.algorithm.bruteForce(self.player1))
                self.playercounter += 1
                self.game.recordMove(self.player1, selection)
            elif (self.playercounter % 2) == 1:
                selection = int(self.algorithm.bruteForce(self.player2))
                self.playercounter += 1
                self.game.recordMove(self.player2, selection)
            self.win, winner = self.game.checkWin()
        except ValueError:
            print('Invalid Move!')
            exit()

        if self.win:
            if winner == self.player1.playercolor:
                self.winner = self.player1
            if winner == self.player2.playercolor:
                self.winner = self.player2

    def minimax(self):
        try:
            if (self.playercounter % 2) == 0:
                selection = int(self.algorithm.minimax(self.player1))
                self.playercounter += 1
                self.game.recordMove(self.player1, selection)
            elif (self.playercounter % 2) == 1:
                selection = int(self.algorithm.minimax(self.player2))
                self.playercounter += 1
                self.game.recordMove(self.player2, selection)
            self.win, winner = self.game.checkWin()
        except ValueError:
            print('Invalid Move!')
            exit()

        if self.win:
            if winner == self.player1.playercolor:
                self.winner = self.player1
            if winner == self.player2.playercolor:
                self.winner = self.player2

    def getWinner(self):
        return self.winner

    def getWinnerColor(self):
        return self.winner.playercolor
