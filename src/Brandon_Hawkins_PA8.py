#-------------------------------------------------------------------------------
# Brandon_Hawkins_PA8.py
# Student Name: Brandon Hawkins
# Assignment: Lab #8
# Submission Date: 11/19/2011
#-------------------------------------------------------------------------------
# Honor Code Statement: I received no assistance on this assignment that
#                       violates the ethical guidelines as set forth by the
#                       instructor and the class syllabus.
#-------------------------------------------------------------------------------

import os

class TooManyLines(BaseException):
    """Thrown when an initial cell state file is longer than expected.
    
    Constructor takes two integers. 
    
    """
    def __init__(self, actual_height, expected_height):
        self.actual_height = actual_height
        self.reported_height = expected_height 
                
    def __str__(self):
        return ("Actual height(%s) is > than expected height(%s)"
                 % (self.actual_height, self.expected_height))

class TooFewLines(BaseException):
    """Thrown when an initial cell state file is shorter than expected.
    
    Constructor takes two integers. 
    
    """
    def __init__(self, actual_height, expected_height):
        self.actual_height = actual_height
        self.expected_height = expected_height 
                
    def __str__(self):
        return ("Actual height(%s) is < than expected height(%s)"
                 % (self.actual_height, self.expected_height))
        
class BadCharacter(BaseException):
    """Thrown when an illegal character is present.
    
    Constructor takes list of strings.
    
    """
    def __init__(self, bad_chars):
        # bad_chars is a list.
        self.bad_chars = bad_chars
    
    def __str__(self):
        return "Bad character(s) encountered: " + str(self.bad_chars)

class BadLineLength(BaseException):
    """Thrown when length of file lines are shorter than expected.
    
    Constructor takes a 2-dim tuple of strings.
    
    """
    def __init__(self, bad_lines):
        self.bad_lines = bad_lines
        
    def __str__(self):
        s = ""
        for line in range (len(self.bad_lines)):
            s += ("\tActual line length(%s) != expected line length(%s) at line(%s)\n" % (self.bad_lines[line]))
        return s
    
def print_dir():
    """Presents the current directory in a readable format"""
    print ("Current directory:\n")
    for dirname, dirnames, filenames in os.walk('.'):
        for subdirname in dirnames:
            print "\t" + os.path.join(dirname, subdirname)
        for filename in filenames:
            if filename.endswith(".txt"):
                print "\t" + os.path.join(dirname, filename) 
            
def get_file():
    """Prompt the user to select a .txt file to parse."""
    print_dir()
    print "\nPlease select a file containing an initial cell state board: " 
    filename = str(raw_input())
    if file_len(filename) < 1:
        print "The file is empty."
        get_file()
    return open(filename, "rU")  

def file_len(filename):
    """Returns the number of lines in a file."""
    with open(filename) as f:
        for i, line in enumerate(f):
            pass
    return i + 1

def get_dimensions():
    """Returns tuple of integers"""
    print "\nPlease enter the height (i.e. - 20) of the board. Must be > 4: "
    height = int(raw_input())
    print "\nPlease enter the width (i.e. - 20) of the board. Must be > 4: "
    width = int(raw_input())
    if height < 5 or width < 5:
        print "Height and width must each be greater than 5"
        get_dimensions()
    return (height, width)
        
def validate_lines(grid, expected_height, expected_width):
    """Check each line contains only valid characters & is expected dimension.
    
    Constructor takes 2-dim list and checks expected line lengths, expected
    height, evaluates each character in the list, and returns void unless
    exceptions are raised.
       
    """
    # String of exceptions that will be built as/if they occur.
    reports = ""
    valid_chars = ("X", ".")
    try:  
        # List of offenses and specific locations.
        bad_chars = []
        for row in range(len(grid)):
            # Check last character of each line is a "\n"
            if grid[row][-1] != "\n":
                bad_chars.append("Line %s does not end with \n" % str(row + 1))
            for char in range(len(grid[row]) - 1):
                # Check all other characters are valid.
                if grid[row][char] not in valid_chars:
                    bad_chars.append(grid[row][char]) 
        # True if bad_chars isn't empty.                   
        if bad_chars:
            raise BadCharacter(bad_chars)
    except BadCharacter as error:
        reports += "\t" + str(error) + "\n"
    
    try:
        # List of offenses and specific locations.
        bad_lines = []
        for row in range(len(grid)):
            # Ignore last element as should be "\n". Checked previously.
            actual_width = len(grid[row]) - 1 
            if actual_width < expected_width or actual_width > expected_width:  
                bad_lines.append((actual_width, expected_width, row + 1))
        # True if bad_lines isn't empty.
        if bad_lines:
            raise BadLineLength(tuple(bad_lines))   
    except BadLineLength as error:
        reports += str(error)
    
    # Store actual height    
    actual_height = len(grid)
        
    try:
        if actual_height > expected_height:
            raise TooManyLines(actual_height, expected_height)
    except TooManyLines as error:
        reports += "\t" + str(error) + "\n"
        
    try:
        if actual_height < expected_height:
            raise TooFewLines(actual_height, expected_height)    
    except TooFewLines as error:
        reports += "\t" + str(error) + "\n"
    
    # True if reports isn't empty.    
    if reports:
        print "File format is invalid. Errors found:\n"
        print reports
    else:
        print "File format okay\n"
       
def main():
    """Confirms file is valid else reports the errors."""
    initial_file = None
    while initial_file == None:
        try:
            initial_file = get_file() 
        except:
            print "That file does not exist."
    
    # Tuple to eventually hold height/width of board.        
    dimensions = ()
    while not dimensions:
        try:
            dimensions = get_dimensions()
        except ValueError:
            print "Must be an integer."
            
    expected_height, expected_width = dimensions[0], dimensions[1]        
    grid = initial_file.readlines()           
    initial_file.close()    
    validate_lines(grid, expected_height, expected_width)
    print "All done!"
    
main()
        

