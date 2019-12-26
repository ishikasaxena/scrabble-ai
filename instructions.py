#Author: ISHIKA SAXENA

import math, copy, string
import random
# cmu_112_graphics_final from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics_final import *
from tkinter import *
from PIL import Image

# instructions screen
class InstructionsMode(Mode):
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill="brown")
        canvas.create_text(mode.width/2, mode.height/10, text='INSTRUCTIONS', fill="#DEB887",
                         font="Helvetica 45 bold")
        startIndent = mode.width/2 - mode.width/10
        startHeight = mode.height/10 + mode.height/15
        canvas.create_text(startIndent, startHeight, 
        text="Welcome to ScrabbleAI, my implementation of Scrabble, \na trademark of Hasbro.",
            fill="#DEB887", font="Helvetica 20 bold")
        nextH1 = startHeight + mode.height/15
        canvas.create_text(startIndent-20, nextH1,
        text="*You can choose to play single player against the AI \n(i.e. computer) or two-player with someone via \nsharing a computer.",
            fill="#DEB887", font="Helvetica 20") 
        nextH2 = nextH1 + mode.height/10
        canvas.create_text(startIndent, nextH2,
        text="*There is a 15 x 15 board. Some squares on the board \nhave colors, indicating multipliers (shown on key in game\n screen)",
            fill="#DEB887", font="Helvetica 20") 
        nextH3 = nextH2 + mode.height/10
        canvas.create_text(startIndent, nextH3,
        text="*Each player gets their own rack of 7 randomly generated \nletters out of a bag of 100 letters.",
            fill="#DEB887", font="Helvetica 20") 
        nextH4 = nextH3 + mode.height/10
        canvas.create_text(startIndent+10, nextH4,
        text="*Each letter has an associated point value, which is helpfully \nwritten on the tiles themselves",
            fill="#DEB887", font="Helvetica 20") 
        nextH5 = nextH4 + mode.height/10
        canvas.create_text(startIndent, nextH5,
        text="*Your objective is to                                                             ", fill="#DEB887", font="Helvetica 20") 
        nextH6 = nextH5 + mode.height/7
        canvas.create_text(startIndent+135, nextH6,
        text='''\
        1) Place a valid word (meaning it’s in the dictionary) on the board to get the most number 
        of points. 
        The player who gets to the most number of points before the bag runs out of tiles 
        wins! This project, ScrabbleAI, uses a 194k word dictionary!
        2) Make sure the location is valid! Each word that you create (except for the first 
        one ever on the board) must be connected/adjacent to other tiles.
        ''',
            fill="#DEB887", font="Helvetica 20") 
        size = (mode.width-mode.width/30) - (mode.width/30)
        canvas.create_rectangle(0, mode.height-mode.height/8, startIndent+size, mode.height-mode.height/20+size,
        fill="#DEB887")
        canvas.create_text(startIndent+40, mode.height-mode.height/20, text='''\
            Ready to play?    
            Click on the SPACE KEY to go back to Home Screen and click PLAY! :)
            If you're in the middle of a game, also click SPACE and PLAY
        '''
        ,fill="brown", font="Helvetica 20 bold")

    def keyPressed(mode, event):
        if event.key == "Space":
            mode.app.setActiveMode(mode.app.splashScreenMode)
