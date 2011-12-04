#------------------------------------------------------------------------------
# Brandon_Hawkins_PP2_cell.py 
# Student Name: Brandon Hawkins 
# Assignment: Project #2
# Submission Date: 11/22/2011 
#------------------------------------------------------------------------------
# Honor Code Statement: I received no assistance on this assignment that 
#                       violates the ethical guidelines as set forth by the 
#                       instructor and the class syllabus. 
#------------------------------------------------------------------------------

class Cell(object):
    """Represents a Cell."""
    def __init__(self, alive):
        """Cell is either alive or dead."""
        self.alive = alive
        
    def __str__(self):
        """If alive, represented by 'X' else represented by '.'"""
        if self.alive:
            return "X"
        return "."
