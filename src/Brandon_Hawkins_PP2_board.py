#------------------------------------------------------------------------------
# Brandon_Hawkins_PP2_board.py 
# Student Name: Brandon Hawkins 
# Assignment: Project #2
# Submission Date: 11/22/2011 
#------------------------------------------------------------------------------
# Honor Code Statement: I received no assistance on this assignment that 
#                       violates the ethical guidelines as set forth by the 
#                       instructor and the class syllabus. 
#------------------------------------------------------------------------------

class Board(object):
    """Represents a game of life grid."""   
    def __init__(self, grid, size):
        # Grid is a dictionary.
        self.grid = grid
        self.board_size = size
        
    def __str__(self):
        """String representation of Board."""  
        result = ""
        for i in range (self.board_size):
            if i > 0:
                result += "\n"
            for j in range(self.board_size):
                result += str(self.grid[(i, j)])
        return result
    
    def get_cell (self, x, y):
        """Returns the Cell at the given position."""
        return self.grid[(x, y)]
    
    def set_cell (self, cell, x, y):
        """Sets the given Cell at the given position."""
        self.grid[(x, y)] = cell
        
    def point_available (self, x, y):
        """Returns True if given position is valid."""
        return (x, y) in self.grid
    
    def would_cell_live (self, x, y):
        """Returns True if Cell would live in the next generation.""" 
        neighbors = 0
        test_cell = self.get_cell(x, y)
        for i in range(3):
            for j in range(3):
                if self.point_available(x - 1 + i, y - 1 + j):
                    curr_cell = self.get_cell(x - 1 + i, y - 1 + j)
                    if curr_cell.alive and curr_cell != test_cell:
                        neighbors += 1
        if test_cell.alive:
            return neighbors == 2 or neighbors == 3
        return neighbors == 3
      
        
