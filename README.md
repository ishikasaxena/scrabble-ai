# scrabble-ai 
## Python Implementation of Word Game Scrabble with AI and Multiplayer Options <br/>
### Project Description <br/>
A Python implementation of the word game Scrabble (product of Hasbro, Inc.) with two modes: Two-Player Mode and AI Mode.
#### Two-Player Mode
Each player has their own rack of 7 randomly generated letters and must form a word on the board that is both in the dictionary and has a valid location (placed words must be connected/adjacent to other words!). <br/>
Each letter has a corresponding point value. The game ends when the bag of letters runs out of tiles. The player who wins when this occurs is the player with more points.
#### AI Mode
The second player is the computer, which attempts to create words with the highest possible points it can create by calculating their raw point value, as well as taking into account their location on the board.

Click [here] for a complete set of rules!

### Installing Any Needed Libraries
1. Make sure you have [Python3] installed
2. Download the files into the same directory
3. All other Libraries (e.g. tkinter) are already installed
4. Run the `runGame.py` file.

[here]:https://scrabble.hasbro.com/en-us/rules
[Python3]:https://www.python.org/download/releases/3.0/
