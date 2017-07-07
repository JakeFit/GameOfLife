import numpy as np
import random
import copy
import os
import Tkinter as tk

class Board(tk.Frame):
    
    def __init__(self, parent, dims):
        self.x = dims[0]
        self.y = dims[1]
        self.board = self.createBoard()
        self.tempBoard = []
        self.size = 8
        
        canvas_width = self.x * self.size
        canvas_height = self.y * self.size 
                
        tk.Frame.__init__(self, parent)
        
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="white")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        
        
    def createBoard(self):
        """
            Create a board with all zero entries.
        """
        board = []
        
        for x in range(self.x):
            board.append([])
            for y in range(self.y):
                board[x].append(0)
                
        return board
    
    def printBoard(self):
        """
            Print the cells of the board
        """
        for row in self.board:
            print row
            
        print ""    
        
    def randomSeed(self, prob):
        """
            Generate live cells on the board as a random seed, with a probability of being alive of prob.
        """
        
        for x in range(self.x):
            for y in range(self.y):
                if not(x == 0 or x == self.x-1 or y == 0 or y == self.y-1):
                    if random.random() < prob:
                        self.board[x][y] = 1

    def inputBoard(self, positions):
        """
            Allow the user to specify a board by supplying a list of positions to be alive.
        """
        for (x,y) in positions:
            self.board[x][y] = 1
            

    def neighbours(self, x, y):
        """
            Gets the value of the neighbours of the point (x,y) and returns them as a list.
            
            Note: Functions on the tempBoard
            
            Goes across neighbouring values left to right, top to bottom.
            
            e.g. 
            e is input point value,
            
            a b c
            d e f
            g h i 
            
            Returns [a, b, c, d, f, g, h, i]
        """
        nbs = []
        dirs = [-1, 0, 1]
        for dirx in dirs:
            for diry in dirs:
                if not((dirx == diry) and (dirx == 0)):
                    nbs.append(self.tempBoard[x + dirx][y + diry])
                    
        return nbs        
            
    def update(self):
        """
            Iterate over the cells of the board and update them according to
            the rules of Conway's Game of Life.
        """
        self.tempBoard = copy.deepcopy(self.board)
        for x in range(1, self.x - 1):
            for y in range(1, self.y - 1):
                # Get value of neighbours
                nbs = sum(self.neighbours(x, y))
                cell = self.tempBoard[x][y] 
                
                # If the cell is dead and has 3 live neighbours, they reporoduce.
                if (cell == 0 and nbs == 3):
                    self.board[x][y] = 1
                    break
                    
                if cell == 1:
                    # Implicit if equal to two or three, lives
                    # Less than two neighbours, dies
                    if nbs < 2:
                        self.board[x][y] = 0
                                                
                    # More than 3 neighbours, dies
                    if nbs > 3:
                        self.board[x][y] = 0
                        
    

if __name__ == '__main__':
    root = tk.Tk()
    
    dims = (10,10)
    gens = 5
    
    board = Board(root, dims)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    root.mainloop()
    
'''board.randomSeed(0.2)
    board.printBoard()
    
    for each in range(gens):
        board.update()
        board.printBoard()'''     