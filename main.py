# Author: Ruslan Huhko
# For: CS Capstone - Fall 2021
# Advisor: Dr. Michael J Reale
# Main Driver Code for Connect Four
# Determines:
# - If two people are playing
# - If AI is playing itself
# - If person is playing computer
# Offers the Following Algorithms:
# - Random
# - Brute Force
# - Minimax w/ Alpha-Beta Pruning

import gameplay
from enum import Enum
import datetime


class PlayerType(Enum):
    MultiHuman = 0
    MultiAI = 1
    ManVsMachine = 2


class AlgorithmType(Enum):
    Random = 0
    BruteForce = 1
    Minimax = 2


def main():
    play = gameplay.Play()

    try:
        for ptype in list(PlayerType):
            print(ptype.name, ': ', ptype.value)
        playerType = PlayerType(int(input('Select Number of Game Type: ')))
    except ValueError:
        print('Invalid Selection')

    if playerType == PlayerType.MultiHuman:
        # print('Human')
        while not play.win:
            play.getNextMove()

    elif playerType == PlayerType.MultiAI:
        try:
            for atype in list(AlgorithmType):
                print(atype.name, ': ', atype.value)
            algorithmType = AlgorithmType(int(input('Select Number of Algorithm: ')))
        except ValueError:
            print('Invalid Selection')

        starttime = datetime.datetime.now()

        if algorithmType == AlgorithmType.Random:
            while not play.win:
                play.random()
        elif algorithmType == AlgorithmType.BruteForce:
            while not play.win:
                play.bruteForce()
        elif algorithmType == AlgorithmType.Minimax:
            while not play.win:
                play.minimax()
        endtime = datetime.datetime.now()
        time = endtime - starttime
        print("Total Time: ", str(time))

    elif playerType == PlayerType.ManVsMachine:
        try:
            print('Red (goes first) - 0\nYellow (goes second) - 1')
            human = int(input('Select numeric value of your which color you desire: '))
            try:
                for atype in list(AlgorithmType):
                    print(atype.name, ': ', atype.value)
                algorithmType = AlgorithmType(int(input('Select Number of Algorithm: ')))
            except ValueError:
                print('Invalid Selection')

            if human == 0:
                while not play.win:
                    if (play.playercounter % 2) == 0:
                        play.getNextMove()
                    elif (play.playercounter % 2) == 1:
                        if algorithmType == AlgorithmType.Random:
                            play.random()
                        elif algorithmType == AlgorithmType.BruteForce:
                            play.bruteForce()
                        elif algorithmType == AlgorithmType.Minimax:
                            play.minimax()
            elif human == 1:
                while not play.win:
                    if (play.playercounter % 2) == 0:
                        if algorithmType == AlgorithmType.Random:
                            play.random()
                        elif algorithmType == AlgorithmType.BruteForce:
                            play.bruteForce()
                        elif algorithmType == AlgorithmType.Minimax:
                            play.minimax()
                    elif (play.playercounter % 2) == 1:
                        play.getNextMove()

        except ValueError:
            print('Invalid Selection')

    play.game.printGame()
    print('The winner is:', play.getWinnerColor())


if __name__ == '__main__':
    main()
