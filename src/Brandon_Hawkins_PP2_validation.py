#-------------------------------------------------------------------------------
# Brandon_Hawkins_PP2_validation.py
# Student Name: Brandon Hawkins
# Assignment: Project #2
# Submission Date: 11/22/2011 
#-------------------------------------------------------------------------------
# Honor Code Statement: I received no assistance on this assignment that
#                       violates the ethical guidelines as set forth by the
#                       instructor and the class syllabus.
#-------------------------------------------------------------------------------

# Constant for square dimensions of grid.
BOARDSIZE = 20

class TooManyLines(BaseException):
    """Thrown when an initial cell state file is longer than expected.
    
    Constructor takes two integers. 
    
    """
    def __init__(self, actual_height, BOARDSIZE):
        self.actual_height = actual_height
        self.reported_height = BOARDSIZE 
                
    def __str__(self):
        return ("Actual height(%s) is > than expected height(%s)"
                 % (self.actual_height, self.BOARDSIZE))

class TooFewLines(BaseException):
    """Thrown when an initial cell state file is shorter than expected.
    
    Constructor takes two integers. 
    
    """
    def __init__(self, actual_height, BOARDSIZE):
        self.actual_height = actual_height
        self.BOARDSIZE = BOARDSIZE 
                
    def __str__(self):
        return ("Actual height(%s) is < than expected height(%s)"
                 % (self.actual_height, self.BOARDSIZE))
        
class BadCharacter(BaseException):
    """Thrown when an illegal character is present.
    
    Constructor takes list of strings.
    
    """
    def __init__(self, bad_chars):
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

class Validation(object):
    """Validate initial cell state file
    
    Constructor takes list of strings.
    
    """
    def __init__(self, grid):
        self.grid = grid
        
    def validate_lines(self):
        """Check each line contains only valid characters & is expected dimension.
        
        Checks expected line lengths, expected
        height, evaluates each character in the list, and returns True unless
        exceptions are raised.
           
        """
        # String of exceptions that will be built as/if they occur.
        reports = ""
        valid_chars = ("X", ".")
        try:  
            # List of offenses and specific locations.
            bad_chars = []
            for row in range(len(self.grid)):
                # Check last character of each line is a "\n"
                if self.grid[row][-1] != "\n":
                    bad_chars.append("Line %s does not end with \n" % str(row + 1))
                for char in range(len(self.grid[row]) - 1):
                    # Check all other characters are valid.
                    if self.grid[row][char] not in valid_chars:
                        bad_chars.append(self.grid[row][char]) 
            # True if bad_chars isn't empty.                   
            if bad_chars:
                raise BadCharacter(bad_chars)
        except BadCharacter as error:
            reports += "\t" + str(error) + "\n"
        
        try:
            # List of offenses and specific locations.
            bad_lines = []
            for row in range(len(self.grid)):
                # Ignore last element as should be "\n". Checked previously.
                actual_width = len(self.grid[row]) - 1 
                if actual_width < BOARDSIZE or actual_width > BOARDSIZE:  
                    bad_lines.append((actual_width, BOARDSIZE, row + 1))
            # True if bad_lines isn't empty.
            if bad_lines:
                raise BadLineLength(tuple(bad_lines))   
        except BadLineLength as error:
            reports += str(error)
        
        # Store actual height    
        actual_height = len(self.grid)
            
        try:
            if actual_height > BOARDSIZE:
                raise TooManyLines(actual_height, BOARDSIZE)
        except TooManyLines as error:
            reports += "\t" + str(error) + "\n"
            
        try:
            if actual_height < BOARDSIZE:
                raise TooFewLines(actual_height, BOARDSIZE)    
        except TooFewLines as error:
            reports += "\t" + str(error) + "\n"
        
        # True if reports isn't empty.    
        if reports:
            print "File format is invalid. Errors found:\n"
            print reports
            return False
        return True
            
                

