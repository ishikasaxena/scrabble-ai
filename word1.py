#NAME: ISHIKA SAXENA

import math, copy, string
import random
# cmu_112_graphics_final taken from 15-112 CMU Fundamentals in Programming & Computer Science Course: 
# Taken from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics_final import *
from tkinter import *
from PIL import Image

# Word class stores the dictionary we're using and has methods to convert it to subsets of different
# word lengths and check word membership
class Word(object):
    # General readFile structure taken from: 
    # http://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
    @staticmethod           
    def readFile(path):
        with open(path, "rt") as f:
            return f.read()

    def __init__(self, word, bag):
        self.word = word.lower()
        # english3.txt taken from: http://www.gwicks.net/dictionaries.htm
        self.contentsRead = Word.readFile("english3.txt")
        self.dictionaryToUse = self.changeDictionaryTxtToSet()
        self.bag = bag  
        self.len34DictSet = self.createLen34Set() # set of len 3 and len 4 words
        self.len4DictSet = self.createLen4Set() # set of len 4 words
        self.len3DictSet = self.createLen3List() # set of len 3 words
        self.len5DictSet = self.createLen5Set() # set of len 5 words
    
    def changeDictionaryTxtToSet(self):
        setToReturn = set()
        for line in self.contentsRead.splitlines():
            setToReturn.add(line)
        return setToReturn
    
    def createLen3List(self):
        setToReturn = set()
        for word in self.dictionaryToUse:
            if len(word) == 3:
                setToReturn.add(word)
        return setToReturn
    
    def createLen4Set(self):
        setToReturn = set()
        for word in self.dictionaryToUse:
            if len(word) == 4:
                setToReturn.add(word)
        return setToReturn
    
    def createLen34Set(self):
        setToReturn = set()
        for word in self.dictionaryToUse:
            if (len(word) == 3) or (len(word) == 4):
                setToReturn.add(word)
        return setToReturn
    
    def createLen5Set(self):
        setToReturn = set()
        for word in self.dictionaryToUse:
            if (len(word) == 5):
                setToReturn.add(word)
        return setToReturn
    
    def checkWordInDictionary(self):
        if self.word in self.dictionaryToUse:
            return True
        else:
            return False