# scrabble-ai 
## Python Implementation of Word Game Scrabble with AI and Multiplayer Options <br/>
### Project Description <br/>
A Python implementation of the word game Scrabble (product of Hasbro, Inc.) with two modes (Two-Player Mode and AI Mode) and a GUI.
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

### How to Run the Project
Run the `runGame.py` file, and ensure that all the files are in the same directory.

### Notes
`english3.txt` is a dictionary downloaded from [here.] <br/>
`cmu_112_graphics_final.py` is from [this] CMU course's (15-112 Fundamentals of Programming and Computer Science) website.

### Snapshot of Game in Action
<img width="791" alt="Screen Shot 2019-12-25 at 7 40 43 PM" src="https://user-images.githubusercontent.com/56605721/71452060-b1138400-274e-11ea-8876-ae47ef70e857.png">

The author is [Ishika Saxena]

[here]:https://scrabble.hasbro.com/en-us/rules
[Python3]:https://www.python.org/download/releases/3.0/
[here.]:http://www.gwicks.net/dictionaries.htm
[this]:https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
[Ishika Saxena]:https://github.com/ishikasaxena
