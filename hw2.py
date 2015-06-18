"""
Clone of 2048 game.
"""

#import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    nonzero = []
    
    for iter1 in range(len(line)):
        if line[iter1] != 0:
            nonzero.append(line[iter1])
    
    results = [0] * len(line)
    for iter2 in range(len(nonzero)):
        results[iter2] = nonzero[iter2]
    
    for iter3 in (range(len(results)-1)):
        if results[iter3] == results[iter3+1]:
            results[iter3] = 2*results[iter3]
            results[iter3+1] = 0
    
    second_nonzero = []
    
    for iter4 in range(len(results)):
        if results[iter4] != 0:
            second_nonzero.append(results[iter4])
    
    final_results = [0] * len(line)
    for iter5 in range(len(second_nonzero)):
        final_results[iter5] = second_nonzero[iter5]
    
    return final_results

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        #self._board = [[0 for dummy_col in range(grid_width)] for dummy_row in range(grid_height)]
        #print self._board
        
        up_key = []
        down_key = []
        left_key = []
        right_key = []
        for dummy_iter1 in range(self._grid_width):
            up_key.append((0,dummy_iter1))
            down_key.append((self._grid_height-1,dummy_iter1))
        for dummy_iter2 in range(self._grid_height):
            left_key.append((dummy_iter2,0))
            right_key.append((dummy_iter2,self._grid_width-1))
        print "ups: ", up_key
        print "downs: ", down_key
        print "lefts: ", left_key
        print "rights: ", right_key
        self._initials = {UP:up_key,DOWN:down_key,LEFT:left_key,RIGHT:right_key}
        
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._board = [[0 for dummy_col in range(self._grid_width)] for dummy_row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()
        #print self.board

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._board)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        count_up_down = 0
        if direction in [UP, DOWN, 1, 2]:
            
            #temp_board = []
            for cell in self._initials[direction]:
                temp_col = []
                for step in range(self._grid_height):
                    row = cell[0] + step * OFFSETS[direction][0]
                    col = cell[1] + step * OFFSETS[direction][1]
                    temp_col.append(self._board[row][col])
                
                replace_col = merge(temp_col)
                
                for step in range(self._grid_height):
                    row = cell[0] + step * OFFSETS[direction][0]
                    col = cell[1] + step * OFFSETS[direction][1]
                    self._board[row][col] = replace_col[step]
                
                if replace_col != temp_col:
                    count_up_down += 1
                
                #for replace_cell in range(self._grid_height):
                    #self._board[cell[0]][replace_cell] = replace_col[replace_cell]
                #temp_board.append(temp_col)
        count_left_right = 0            
        if direction in [LEFT, RIGHT, 3, 4]:
            
            #temp_board = []
            for cell in self._initials[direction]:
                temp_row = []
                for step in range(self._grid_width):
                    row = cell[0] + step * OFFSETS[direction][0]
                    col = cell[1] + step * OFFSETS[direction][1]
                    temp_row.append(self._board[row][col])
                
                replace_row = merge(temp_row)
                
                for step in range(self._grid_width):
                    row = cell[0] + step * OFFSETS[direction][0]
                    col = cell[1] + step * OFFSETS[direction][1]
                    self._board[row][col] = replace_row[step]
                
                if replace_row != temp_row:
                    count_left_right += 1
                
                #for replace_cell in range(self._grid_width):
                    #self._board[cell[1]][replace_cell] = replace_row[replace_cell]
                #temp_board.append(temp_row)
        
        if (count_up_down != 0) or (count_left_right != 0):
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        pick_row = random.randrange(0, self._grid_height)
        pick_column = random.randrange(0, self._grid_width)
        #print "row: ", pick_row
        #print "column: ", pick_column
        two_or_four = random.randrange(0,10)
        #print "two or four: ", two_or_four
        if self._board[pick_row][pick_column] == 0:
            if two_or_four == 0:
                #print "dice for 4: ", two_or_four
                self._board[pick_row][pick_column] = 4
            else:
                #print "dice for 2: ", two_or_four
                self._board[pick_row][pick_column] = 2
        else:
            self.new_tile()
        #print self.board

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._board[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._board[row][col]

#TwentyFortyEight(4,5)
    
#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
