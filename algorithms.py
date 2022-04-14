# Author: Ruslan Huhko
# For: CS Capstone - Fall 2021
# Advisor: Dr. Michael J Reale
# Contains gameplay algorithms:
# - Random
# - BruteForce
# - Minimax

import random
import numpy as np
import truthtable
import networkx as nx
import matplotlib.pyplot as plt
import gameboard
import math


class Algorithm:

    def __init__(self, gameboard):
        self.gameboard = gameboard

    def random(self):
        # randomly selects one of the available locations until four in a row exists
        # returns int selection
        posList = self.checkAvailPos(self.gameboard, as_tuple=False)
        return random.choice(posList)

    def checkAvailPos(self, gameboard, as_tuple):
        # Returns list of available columns to choose from [0-6]
        # Or returns list of position coordinates held by either player
        posList = []
        rList = []
        yList = []
        for c in range(gameboard.shape[1]):
            for r in reversed(range(gameboard.shape[0])):
                if gameboard[r, c].isdigit():
                    posList.append(int(c))
                    break
                elif gameboard[r, c] == 'R':
                    rList.append((r, c))
                elif gameboard[r, c] == 'Y':
                    yList.append((r, c))

        if as_tuple:
            # Returns list of tuples for positions
            return rList, yList
        else:
            return posList

    def bruteForce(self, player):
        # Driver Code for Brute Force
        # Determines next position based on the least moves necessary to achieve a winning combination
        # Returns selection 0-6
        """
        # Code using the Bruteforce Class
        bruteforce = BruteForce(self.gameboard)
        bruteforce.main(player)

        # For debugging
        bruteforce.printGraph()
        print(nx.info(bruteforce.graph))

        bruteforce.clearGraph()
        selection = bruteforce.returnSelection()
        # print(selection, ": Player", player.playercolor)
        """

        # Code using the bruteforce minimax
        bruteforce = Minimax(self.gameboard, depth=math.inf)
        playercolor = player.playercolor

        if playercolor == 'R':
            col, weight = bruteforce.bruteForce(self.gameboard, True, False)
        elif playercolor == 'Y':
            col, weight = bruteforce.bruteForce(self.gameboard, False, False)

        selection = col

        return selection

    def minimax(self, player):
        # Driver Code for Minimax
        # Returns selection 0-6
        minimax = Minimax(self.gameboard, depth=4)
        minimax.main(player)

        selection = minimax.returnSelection()
        return selection


class Minimax(Algorithm):

    def __init__(self, cur_gameboard, depth):
        self.gameboard = cur_gameboard.copy()
        self.depth = depth
        self.selection = None
        self.alpha = -math.inf
        self.beta = math.inf

    def getScore(self, gameboard, isMaximizingPlayer):
        # Sets weights/scores for nodes
        # Code recycled from truthtable.py

        if isMaximizingPlayer:
            player = 'R'
            opp_player = 'Y'
        elif not isMaximizingPlayer:
            player = 'Y'
            opp_player = 'R'

        score = 0

        templist = []

        # all horizontal positions
        for r in range(6):
            for c in range(4):
                horizontal = gameboard[r, c:(c + 4)]
                count = 0
                opp_count = 0
                for i in horizontal:
                    if i == player:
                        count += 1
                    elif i == opp_player:
                        opp_count -= 1
                if count == 4:
                    score += 100
                elif opp_count == 0:
                    score += count
                if opp_count == 3:
                    score -= 100
                else:
                    score -= opp_count * 4

        # all vertical positions
        for r in range(3):
            for c in range(7):
                vertical = gameboard[r:(r + 4), c]
                count = 0
                opp_count = 0
                for i in vertical:
                    if i == player:
                        count += 1
                    elif i == opp_player:
                        opp_count -= 1
                if count == 4:
                    score += 100
                elif opp_count == 0:
                    score += count
                if opp_count == 3:
                    score -= 100
                else:
                    score -= opp_count * 4

        # positive diagonal
        for r in range(3):
            for c in range(4):
                for i in range(4):
                    truepos = gameboard[(r + 3 - i), (c + i)]
                    templist.append(str(truepos))
                positive = np.array(templist)
                count = 0
                opp_count = 0
                for i in positive:
                    if i == player:
                        count += 1
                    elif i == opp_player:
                        opp_count -= 1
                templist.clear()
                if count == 4:
                    score += 100
                elif opp_count == 0:
                    score += count
                if opp_count == 3:
                    score -= 100
                else:
                    score -= opp_count * 4

        # negative diagonal
        for r in range(3):
            for c in range(4):
                for i in range(4):
                    truepos = gameboard[(r + i), (c + i)]
                    templist.append(str(truepos))
                negative = np.array(templist)
                count = 0
                opp_count = 0
                for i in negative:
                    if i == player:
                        count += 1
                    elif i == opp_player:
                        opp_count -= 1
                templist.clear()
                if count == 4:
                    score += 100
                elif opp_count == 0:
                    score += count
                if opp_count == 3:
                    score -= 100
                else:
                    score -= opp_count * 4

        # Add more weight to center row
        # Done manually since not training
        for r in range(3):
            vertical = gameboard[r:(r + 4), 3]
            count = 0
            opp_count = 0
            for i in vertical:
                if i == player:
                    count += 1
                elif i == opp_player:
                    opp_count -= 1
            if count == 4:
                score += 100
            elif opp_count == 0:
                score += count
            if opp_count == 3:
                score -= 100
            else:
                score -= opp_count * 4

        if isMaximizingPlayer:
            return score
        elif not isMaximizingPlayer:
            return -score

    def recordMove(self, gameboard, player, column):
        # Records move in lowest row within given column
        # Code recycled from gameboard.py not to prevent continual creation of Gameboard objects

        for i in reversed(range(gameboard.shape[0])):
            if gameboard[i, column].isalpha():
                if i == 0:
                    # Raises Error if the selected column is full
                    raise ValueError
                else:
                    continue
            else:
                gameboard[i, column] = player
                break
        return gameboard

    def minimax(self, board, depth, isMaximizingPlayer, alpha, beta):
        # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
        # Red is always maximizing player
        # Yellow is always minimizing player

        availCol = self.checkAvailPos(board, as_tuple=False)
        if len(availCol) == 0:
            return None, None
        col = availCol[0]  # Default Value

        if depth == 0:
            return None, self.getScore(board, isMaximizingPlayer)

        if isMaximizingPlayer:
            max_val = -math.inf
            for c in availCol:
                board_copy = board.copy()  # because python passes by reference
                board_copy = self.recordMove(board_copy, 'R', c)
                opp_col, score = self.minimax(board_copy, (depth - 1), False, alpha, beta)
                if score > max_val:
                    max_val = score
                    col = c
                alpha = max(alpha, max_val)
                if alpha >= beta:
                    break
            return col, max_val
        elif not isMaximizingPlayer:
            min_val = math.inf
            for c in availCol:
                board_copy = board.copy()  # because python passes by reference
                board_copy = self.recordMove(board_copy, 'Y', c)
                opp_col, score = self.minimax(board_copy, (depth - 1), True, alpha, beta)
                if score < min_val:
                    min_val = score
                    col = c
                beta = min(beta, min_val)
                if alpha >= beta:
                    break
            return col, min_val

    def bruteForce(self, board, isMaximizingPlayer, isFinalMove):
        # BruteForce Approach
        # Basically Minimax without depth limit, and alpha-beta pruning
        # Red is always maximizing player
        # Yellow is always minimizing player

        availCol = self.checkAvailPos(board, as_tuple=False)

        if isFinalMove:
            return None, self.getScore(board, isMaximizingPlayer)

        if len(availCol) == 0:
            # Board is complete
            return None, self.getScore(board, isMaximizingPlayer)
        col = availCol[0]  # Default Value

        if isMaximizingPlayer:
            max_val = -math.inf
            for col in range(len(availCol)):
                c = availCol[col]
                if col == len(availCol):
                    isFinalMove = True
                else:
                    isFinalMove = False
                board_copy = board.copy()  # because python passes by reference
                board_copy = self.recordMove(board_copy, 'R', c)
                opp_col, score = self.bruteForce(board_copy, False, isFinalMove)
                if score > max_val:
                    max_val = score
                    col = c
                # alpha = max(alpha, max_val)
                # if alpha >= beta:
                #    break
            return col, max_val
        elif not isMaximizingPlayer:
            min_val = math.inf
            for col in range(len(availCol)):
                c = availCol[col]
                if col == len(availCol):
                    isFinalMove = True
                else:
                    isFinalMove = False
                board_copy = board.copy()  # because python passes by reference
                board_copy = self.recordMove(board_copy, 'Y', c)
                opp_col, score = self.bruteForce(board_copy, True, isFinalMove)
                if score < min_val:
                    min_val = score
                    col = c
                # beta = min(beta, min_val)
                # if alpha >= beta:
                #    break
            return col, min_val

    def returnSelection(self):
        return self.selection

    def main(self, player):
        # Driver Code for this class
        playercolor = player.playercolor

        if playercolor == 'R':
            col, weight = self.minimax(self.gameboard, self.depth, True, self.alpha, self.beta)
        elif playercolor == 'Y':
            col, weight = self.minimax(self.gameboard, self.depth, False, self.alpha, self.beta)

        self.selection = col

        return


class BruteForce(Algorithm):

    def __init__(self, cur_gameboard):
        self.graph = nx.MultiGraph()
        self.gameboard = cur_gameboard
        self.truthtable = truthtable.TruthTable()
        self.gameboardTemplate = np.arange(42).reshape(6, 7)
        self.selection = None
        self.player = None
        self.board = gameboard.GameBoard()

        # Begins with each player having own array of potential winning combinations
        self.rTruth = self.truthtable.returntruthtable()
        self.yTruth = self.truthtable.returntruthtable()
        self.truthTableArray = self.truthtable.returntruthtable()

    def choosePath(self):
        # Iterates over graph to find the best path
        # Returns list of nodes for path
        possible_paths = []

        # Traverse possible paths
        for path_array in self.truthTableArray:
            # connvert path array into list
            path = path_array.tolist()

            try:
                if nx.is_path(self.graph, path):
                    possible_paths.append(path)
            except KeyError:
                pass

        # find the weights for the paths
        weights = []
        for path in possible_paths:
            weights.append(nx.path_weight(self.graph, path, weight="weight"))

        # Choose the path with the lowest weight
        # If multiple paths with lowest weight, chooses the first to be tested
        lowest_weight = 100
        lowest_weight_pos = None
        for i in range(len(weights)):
            weight = weights[i]
            if weight < lowest_weight:
                lowest_weight = weight
                lowest_weight_pos = i

        # Choose path with the lowest weight
        best_path = possible_paths[lowest_weight_pos]

        return best_path

    def returnSelection(self):
        # Returns Next Selection
        # Takes position number and converts to column number
        for r in range(self.gameboardTemplate.shape[0]):
            for c in range(self.gameboardTemplate.shape[1]):
                if self.selection == self.gameboardTemplate[r, c]:
                    return c
        return None

    def curPositions(self, curList, oppList):
        # Converts list of tuples into list of positions [0-41]
        curPos = []

        for pos in curList:
            r, c = pos
            curPos.append(self.gameboardTemplate[r, c])
        # List of Positions taken by opponent
        oppPos = []
        for pos in oppList:
            r, c = pos
            oppPos.append(self.gameboardTemplate[r, c])

        return curPos, oppPos

    def getNextAvailPos(self, board):
        # Get next available positions
        # If column is full, sets 9 for row
        # Returns array of coordinates for next available positions
        nextAvailPos = np.zeros((board.shape[1], 2), dtype=int)
        for c in range(board.shape[1]):
            nextAvailPos[c, 1] = c
            for r in range(board.shape[0]):
                if board[r, c].isalpha():
                    if r == 0:
                        # Column is full
                        nextAvailPos[c, 0] = 9  # Number is out of bounds
                    break
                else:
                    if nextAvailPos[c, 0] < r:
                        nextAvailPos[c, 0] = r
        return nextAvailPos

    def takenByOpp(self, pos, oppPosList):
        # Checks if position in question is an available option
        for opp in oppPosList:
            if pos == opp:
                return True
        return False

    def adjacentPositions(self, templatePosNumber):
        # returns list of all adjacent position numbers
        # Determine location of current position
        loc = np.where(self.gameboardTemplate == templatePosNumber)
        r, c = loc
        r = int(r)
        c = int(c)

        adjList = []
        try:
            if (c - 1) < 0:
                raise IndexError
            l = self.gameboardTemplate[r, c - 1]
            adjList.append(l)
        except IndexError:
            pass
        try:
            if ((r - 1) < 0) or ((c - 1) < 0):
                raise IndexError
            nd = self.gameboardTemplate[r - 1, c - 1]
            adjList.append(nd)
        except IndexError:
            pass
        try:
            if (r - 1) < 0:
                raise IndexError
            v = self.gameboardTemplate[r - 1, c]
            adjList.append(v)
        except IndexError:
            pass
        try:
            if (r - 1) < 0:
                raise IndexError
            pd = self.gameboardTemplate[r - 1, c + 1]
            adjList.append(pd)
        except IndexError:
            pass
        try:
            r = self.gameboardTemplate[r, c + 1]
            adjList.append(r)
        except IndexError:
            pass
        try:
            nnd = self.gameboardTemplate[r + 1, c + 1]
            adjList.append(nnd)
        except IndexError:
            pass
        try:
            nv = self.gameboardTemplate[r + 1, c]
            adjList.append(nv)
        except IndexError:
            pass
        try:
            if (c - 1) < 0:
                raise IndexError
            npd = self.gameboardTemplate[r + 1, c - 1]
            adjList.append(npd)
        except IndexError:
            pass

        return adjList

    def addEdges(self, curList, oppList):
        # Creates the graph
        # Connects the nodes for potential moves
        curPos, oppPos = self.curPositions(curList, oppList)

        # Connect existing nodes using curPos
        for pos in curPos:

            # Determine adjacent positions
            test_list = self.adjacentPositions(pos)

            # Check list against opponent's positions
            to_del = []
            for testpos in oppPos:
                for adj in test_list:
                    if adj == testpos:
                        to_del.append(adj)
            for i in to_del:
                test_list.remove(i)

            # Add Existing Edges
            for testpos in curPos:
                for adj in test_list:
                    if adj == testpos:
                        self.graph.add_edge(pos, adj, weight=0)

        # Create Board for potential moves
        self.board.gameboard = self.gameboard.copy()

        # Create Graph
        weight_counter = 0
        no_more_moves = False
        while not no_more_moves:
            weight_counter += 1
            # Get Coordinates for Next Available Positions
            nextAvailPos = self.getNextAvailPos(self.board.gameboard)

            # Check if all columns are full
            # Remove elements of array that are out of bounds
            to_del = []
            for i in range(nextAvailPos.shape[0]):
                r, c = nextAvailPos[i]
                if r == 9:
                    to_del.append(i)
            # Break Condition
            if len(to_del) == nextAvailPos.shape[0]:
                no_more_moves = True
                break
            else:
                for i in reversed(to_del):
                    nextAvailPos = np.delete(nextAvailPos, i, axis=0)

            # Connect Edges to Next Available Positions
            for coord in nextAvailPos:
                r, c = coord
                pos = self.gameboardTemplate[r, c]

                # Determine adjacent positions
                adj_list = self.adjacentPositions(pos)

                # Check list against opponent's positions
                to_del = []
                for testpos in oppPos:
                    for adj in adj_list:
                        if adj == testpos:
                            to_del.append(adj)
                for i in to_del:
                    adj_list.remove(i)

                # Add Edges
                for adj_pos in adj_list:
                    self.graph.add_edge(pos, adj_pos, weight=weight_counter)

                # Update theoretical gameboard
                try:
                    self.board.recordMove(self.player, c)
                except ValueError:
                    pass

    def printGraph(self):
        # Saves and displays the graph for the next possible move
        # Uses whichever graph was saved last
        # Detailed/labelled graph requires too much memory
        nx.draw(self.graph)
        plt.savefig("BruteForceGraph.png")
        plt.show()

    def clearGraph(self):
        # Graph Destructor Method
        # Clears the Graph
        # Not included in main method, so the printGraph method can still be called
        self.graph.clear_edges()

    def main(self, player):
        # Brute Force Selection
        # Determines next position based on the least moves necessary to achieve a winning combination
        self.player = player
        rPos, yPos = self.checkAvailPos(self.gameboard, as_tuple=True)

        # Create Graph of possible winning combinations
        if player.playercolor == 'R':
            self.addEdges(rPos, yPos)

        elif player.playercolor == 'Y':
            self.addEdges(yPos, rPos)

        # Do Bruteforce
        selected_path = self.choosePath()

        # Paths should already be sorted
        self.selection = selected_path[0]

