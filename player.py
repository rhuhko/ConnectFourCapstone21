# Author: Ruslan Huhko
# For: CS Capstone - Fall 2021
# Advisor: Dr. Michael J Reale
# Definition class for the 2 players

class Player:

    def __init__(self, playercolor):
        # Designed to store player color
        if playercolor is None:
            # For Debugging and Tie
            self.playercolor = "No Winner"
        else:
            self.playercolor = str(playercolor)
